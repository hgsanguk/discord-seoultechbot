import datetime
import discord
import os
import server_bot_settings
import menucrawler
from discord.ext import commands, tasks

game = discord.Game('명령어: /도움')
bot = commands.Bot(command_prefix='/', intents=discord.Intents.all())
notification_time = [datetime.time(hour=i, minute=0, tzinfo=datetime.timezone(datetime.timedelta(hours=9))) for i in range(9, 13)]
crawling_time = [datetime.time(hour=i, minute=0, tzinfo=datetime.timezone(datetime.timedelta(hours=9))) for i in range(0, 18, 2)]


@bot.event
async def on_ready():
    print('봇 실행 완료')
    server_bot_settings.initial()
    menucrawler.initial()
    crawling.start()
    food_notification.start()
    await crawling()
    await bot.change_presence(status=discord.Status.online, activity=game)


@bot.command(name="2학")
async def _2학(ctx):
    try:
        today = datetime.datetime.now()
        food_data = menucrawler.get_sc2_menu(int(today.strftime('%y%m%d')))
        embed = discord.Embed(title="제2학생회관", description=today.strftime("%m월 %d일 식단표"))
        embed.add_field(name=f"{food_data[0]} `{food_data[1]}`", value=f"{food_data[2]}", inline=False)
        embed.add_field(name=f"{food_data[3]} `{food_data[4]}`", value=f"{food_data[5]}", inline=False)
        await ctx.send(embed=embed)
    except IndexError:
        embed = discord.Embed(title="제2학생회관", description='오늘 등록된 점심 식단표가 없습니다.')
        await ctx.send(embed=embed)


@bot.command()
async def 테파(ctx):
    today = datetime.datetime.now()
    food_data = menucrawler.get_technopark_menu(int(today.strftime('%y%W')))
    embed = discord.Embed(title="테크노파크", description=f"{food_data[0]}")
    embed.set_image(url=f"{food_data[1]}")
    await ctx.send(embed=embed)


@bot.command()
async def 도움(ctx):
    embed = discord.Embed(title="봇 명령어 목록")
    embed.add_field(name=':warning:주의사항:warning:', value='**봇 입장 후 `/알림설정` 명령어를 사용해야 봇 & 학교 공지사항을 받을 수 있습니다.**\n'
                                                            '학교 공지사항은 학교 홈페이지의 **대학공지사항, 학사공지, 장학공지**를 알려드립니다. '
                                                            '이외의 공지사항은 학교 홈페이지를 참고하시기 바랍니다.\n', inline=False)
    embed.add_field(name='`/2학`', value='제2학생회관의 오늘 식단표를 출력합니다.', inline=False)
    embed.add_field(name='`/테파`', value='테크노파크의 이번 주 식단표를 출력합니다.', inline=False)
    embed.add_field(name='`/알림설정 (0, 9 ~ 12)`', value='해당 명령어를 입력한 채널이 학교 공지사항, 봇 공지사항과 학식 알림을 받을 채널이 됩니다.\n'
                                                        '9 ~ 12 사이의 정수를 입력하여 학식 알림을 받을 시간대를 설정할 수 있으며, '
                                                        '0을 입력하거나 정수를 입력하지 않을 경우 학식 알림을 보내지 않습니다.', inline=False)
    await ctx.send(embed=embed)


@bot.command()
async def 알림설정(ctx, arg='0'):
    try:
        arg = int(arg)
        if arg == 0:
            server_bot_settings.set_notification_channel(ctx.guild.id, ctx.channel.id, arg)
            await ctx.send(':white_check_mark: 이제부터 이 채널에서 봇 공지사항과 학교 공지사항을 알려드립니다.')
        elif 9 <= arg <= 12:
            server_bot_settings.set_notification_channel(ctx.guild.id, ctx.channel.id, arg)
            await ctx.send(f':white_check_mark: 이제부터 이 채널에서 봇 공지사항과 학교 공지사항, 그리고 매일 {arg}시에 학식 메뉴를 알려드립니다.')
        else:
            raise ValueError
    except ValueError:
        await ctx.send(':no_entry_sign: 올바르지 않은 입력입니다. 9 이상 12 이하의 정수를 입력하세요.')


@tasks.loop(time=crawling_time)
async def crawling():
    today = datetime.datetime.now()
    if today.weekday() < 5:
        try:
            menucrawler.get_sc2_menu(int(today.strftime('%y%m%d')))
        except IndexError:
            menucrawler.student_cafeteria_2()
        try:
            menucrawler.get_technopark_menu(int(today.strftime('%y%W')))
        except IndexError:
            menucrawler.technopark()


@tasks.loop(time=notification_time)
async def food_notification():
    today = datetime.datetime.now()
    for channel_id in server_bot_settings.get_channel(today.hour):
        try:
            channel = bot.get_channel(channel_id)
            await 테파(channel)
            await _2학(channel)
        except Exception:
            continue


@bot.command()
async def 테스트(ctx):
    today = datetime.datetime.now()
    for channel_id in server_bot_settings.get_channel(10):
        try:
            channel = bot.get_channel(channel_id)
            await _2학(channel)
            await 테파(channel)
        except Exception:
            continue


bot.run(os.getenv('DiscordBotToken'))  # Insert Your Bot Token
