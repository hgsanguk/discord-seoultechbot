import datetime
import discord
import os
import server_bot_settings
import menucrawler
import noticecrawler
import weather
from itertools import cycle
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions, MissingPermissions

token_path = os.path.dirname(os.path.abspath(__file__)) + "/token.txt"
token_file = open(token_path, "r", encoding="utf-8").read().split()
discord_bot_token = token_file[0]
weather_api_token = token_file[1]

print("Discord Bot Token: ", discord_bot_token)
print("오픈 API 기상청 단기예보 조회서비스 Token: ", weather_api_token)

bot = commands.Bot(command_prefix='/', intents=discord.Intents.all())
global status
CRAWLING_PERIOD = 2
BOT_VERSION = 'v1.0-beta3'
food_notification_time = [datetime.time(hour=i, minute=0,
                                        tzinfo=datetime.timezone(datetime.timedelta(hours=9))) for i in range(9, 13)]
notice_crawling_time = [datetime.time(hour=i, minute=30,
                                      tzinfo=datetime.timezone(datetime.timedelta(hours=9))) for i in range(1, 24, CRAWLING_PERIOD)]
food_crawling_time = [datetime.time(hour=i, minute=0,
                                    tzinfo=datetime.timezone(datetime.timedelta(hours=9))) for i in range(0, 24, CRAWLING_PERIOD)]


@bot.event
async def on_ready():
    # DB 초기화
    server_bot_settings.initial()
    menucrawler.initial()
    noticecrawler.initial()

    # task 시작
    food_crawling.start()
    notice_crawling.start()
    food_notification.start()
    change_status.start()
    global status
    status = cycle(['명령어: /도움', f'{BOT_VERSION}', f'{len(bot.guilds)}개의 서버와 함께'])

    noticecrawler.univ_notice()
    noticecrawler.affairs_notice()
    noticecrawler.scholarship_notice()

    await food_crawling()
    await bot.change_presence(status=discord.Status.online)
    print('봇 실행 완료.')


@bot.command(name="2학")
async def _2학(ctx):
    try:
        today = datetime.datetime.now()
        day_str = '{today.month}월 {today.day}일 식단표'.format(today=today)
        food_data = menucrawler.get_sc2_menu(int(today.strftime('%y%m%d')))
        embed = discord.Embed(title="제2학생회관", description=day_str, color=0x73BF1F)
        embed.add_field(name=f"{food_data[0]} `{food_data[1]}`", value=f"{food_data[2]}", inline=False)
        embed.add_field(name=f"{food_data[3]} `{food_data[4]}`", value=f"{food_data[5]}", inline=False)
        embed.add_field(name=f"{food_data[6]}(저녁) `{food_data[7]}`", value=f"{food_data[8]}", inline=False)
        await ctx.send(embed=embed)
    except IndexError:
        embed = discord.Embed(title="제2학생회관", description='오늘 등록된 식단표가 없습니다.')
        await ctx.send(embed=embed)


@bot.command()
async def 테파(ctx):
    try:
        today = datetime.datetime.now()
        food_data = menucrawler.get_technopark_menu(int(today.strftime('%y%W')))
        embed = discord.Embed(title="테크노파크", description=f"{food_data[0]}", color=0x0950A1)
        embed.set_image(url=f"{food_data[1]}")
        await ctx.send(embed=embed)
    except IndexError:
        embed = discord.Embed(title="테크노파크", description='이번 주에 등록된 식단표가 없습니다.')
        await ctx.send(embed=embed)


@bot.command()
async def 날씨(ctx, args='0'):
    try:
        args = int(args)
        if 0 <= args < 5:
            data = weather.get_weather(weather_api_token, args)

            if 8 <= data[0].hour <= 16:
                color = 0x99CCFF
            elif 5 <= data[0].hour < 8:
                color = 0xFAEBD7
            elif 16 < data[0].hour < 19:
                color = 0xF29886
            else:
                color = 0x000080

            embed = discord.Embed(title="오늘의 캠퍼스 날씨",
                                  description='{day.month}월 {day.month}일 {day.hour}시 {day.minute}분 공릉동의 날씨입니다.'
                                  .format(day=data[0]), color=color)

            if data[2][3] == '1':
                embed.add_field(name=':umbrella: 비\n'
                                     ':cloud_snow: 강수량 :' + data[2][4] + '\n'
                                     ':thermometer: 기온: ' + data[2][0] + '°C',
                                value=':droplet: 습도: ' + data[2][5] + '%\n'
                                      ':dash: 바람: ' + data[2][7] + '(' + data[2][6] + '°) 방향으로 ' + data[2][8] + 'm/s',
                                inline=False)
            elif data[2][3] == '2':
                embed.add_field(name=':umbrella: 눈비\n'
                                     ':cloud_snow: 강수량 :' + data[2][4] + '\n'
                                     ':thermometer: 기온: ' + data[2][0] + '°C',
                                value=':droplet: 습도: ' + data[2][5] + '%\n'
                                      ':dash: 바람: ' + data[2][7] + '(' + data[2][6] + '°) 방향으로 ' + data[2][8] + 'm/s',
                                inline=False)
            elif data[2][3] == '3':
                embed.add_field(name=':snowman2: 눈\n'
                                     ':cloud_snow: 강수량 :' + data[2][4] + '\n'
                                     ':thermometer: 기온: ' + data[2][0] + '°C',
                                value=':droplet: 습도: ' + data[2][5] + '%\n'
                                      ':dash: 바람: ' + data[2][7] + '(' + data[2][6] + '°) 방향으로 ' + data[2][8] + 'm/s',
                                inline=False)
            elif data[2][3] == '4':
                embed.add_field(name=':white_sun_rain_cloud: 소나기\n'
                                     ':cloud_snow: 강수량 :' + data[2][4] + '\n'
                                     ':thermometer: 기온: ' + data[2][0] + '°C',
                                value=':droplet: 습도: ' + data[2][5] + '%\n'
                                      ':dash: 바람: ' + data[2][7] + '(' + data[2][6] + '°) 방향으로 ' + data[2][8] + 'm/s',
                                inline=False)
            elif data[2][3] == '5':
                embed.add_field(name=':sweat_drops: 빗방울\n'
                                     ':cloud_snow: 강수량 :' + data[2][4] + '\n'
                                     ':thermometer: 기온: ' + data[2][0] + '°C',
                                value=':droplet: 습도: ' + data[2][5] + '%\n'
                                      ':dash: 바람: ' + data[2][7] + '(' + data[2][6] + '°) 방향으로 ' + data[2][8] + 'm/s',
                                inline=False)
            elif data[2][3] == '6':
                embed.add_field(name=':umbrella: 싸락눈/빗방울\n'
                                     ':cloud_snow: 강수량 :' + data[2][4] + '\n'
                                     ':thermometer: 기온: ' + data[2][0] + '°C',
                                value=':droplet: 습도: ' + data[2][5] + '%\n'
                                      ':dash: 바람: ' + data[2][7] + '(' + data[2][6] + '°) 방향으로 ' + data[2][8] + 'm/s',
                                inline=False)
            elif data[2][3] == '7':
                embed.add_field(name=':snowflake: 싸락눈\n'
                                     ':cloud_snow: 강수량 :' + data[2][4] + '\n'
                                     ':thermometer: 기온: ' + data[2][0] + '°C',
                                value=':droplet: 습도: ' + data[2][5] + '%\n'
                                      ':dash: 바람: ' + data[2][7] + '(' + data[2][6] + '°) 방향으로 ' + data[2][8] + 'm/s',
                                inline=False)
            else:
                embed.add_field(name=data[2][2] + '\n:thermometer: 기온: ' + data[2][0] + '°C',
                                value=':droplet: 습도: ' + data[2][5] + '%\n:dash: 바람: ' + data[2][7] + '(' + data[2][6]
                                      + '°) 방향으로 ' + data[2][8] + 'm/s', inline=False)

            embed.set_footer(text='기상청 초단기예보 조회 서비스 오픈 API를 이용한 것으로, 실제 기상상황과 차이가 있을 수 있습니다.')
            await ctx.send(embed=embed)
        else:
            raise ValueError
    except ValueError:
        await ctx.send(':no_entry_sign: 올바르지 않은 입력입니다. 4 이하의 정수를 입력하세요.')
    except Exception:
        await ctx.send('날씨 정보를 불러오는 중 오류가 발생했습니다.')


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
    embed.add_field(name='`/날씨 (0 ~ 4)`', value='0 ~ 4시간 뒤의 날씨 예보를 출력합니다.\n숫자를 입력하지 않는 경우 현재 날씨 예보를 출력합니다.(`/날씨 0`과 동일)', inline=False)
    await ctx.send(embed=embed)


@bot.command()
@has_permissions(administrator=True, manage_messages=True)
async def 알림설정(ctx, arg='0'):
    try:
        arg = int(arg)
        if arg == 0:
            server_bot_settings.set_notification_channel(ctx.guild.id, ctx.channel.id, arg)
            print(f'{ctx.guild.name}({ctx.guild.id}) 서버의 {ctx.channel.name}({ctx.channel.id}) 채널에서 알림 받을 채널 설정. 학식 알림 받지 않음.')
            await ctx.send(':white_check_mark: 이제부터 이 채널에서 봇 공지사항과 학교 공지사항을 알려드립니다.')
        elif 9 <= arg <= 12:
            server_bot_settings.set_notification_channel(ctx.guild.id, ctx.channel.id, arg)
            print(f'{ctx.guild.name}({ctx.guild.id}) 서버의 {ctx.channel.name}({ctx.channel.id}) 채널에서 알림 받을 채널 설정. 학식 알림 시간: {arg}시')
            await ctx.send(f':white_check_mark: 이제부터 이 채널에서 봇 공지사항과 학교 공지사항, 그리고 매일 {arg}시에 학식 메뉴를 알려드립니다.')
        else:
            raise ValueError
    except ValueError:
        await ctx.send(':no_entry_sign: 올바르지 않은 입력입니다. 9 이상 12 이하의 정수를 입력하세요.')


@알림설정.error
async def 알림설정_error(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.message.channel.send(':no_entry: 해당 명령어를 실행할 권한이 없습니다.')


@tasks.loop(time=food_crawling_time)
async def food_crawling():
    today = datetime.datetime.now()
    if today.weekday() < 5:
        try:
            menucrawler.get_sc2_menu(int(today.strftime('%y%m%d')))
        except IndexError:
            print(f'{today}에 제2학생회관 식단 크롤링 시도...')
            menucrawler.student_cafeteria_2()
        try:
            menucrawler.get_technopark_menu(int(today.strftime('%y%W')))
        except IndexError:
            print(f'{today}에 서울테크노파크 식단 크롤링 시도...')
            menucrawler.technopark()


@tasks.loop(time=notice_crawling_time)
async def notice_crawling():
    channels = server_bot_settings.get_channel_all()
    try:
        new_univ_notice = noticecrawler.univ_notice()
        new_affairs_notice = noticecrawler.affairs_notice()
        new_scholarship_notice = noticecrawler.scholarship_notice()
    except ConnectionError:
        new_univ_notice = []
        new_affairs_notice = []
        new_scholarship_notice = []
        print('학교 홈페이지 연결 실패. 다음 주기에 다시 시도합니다.')

    if len(channels) > 0:
        if len(new_univ_notice) > 0:
            embed = discord.Embed(title="새 대학공지사항", color=0xA4343A)
            for row in new_univ_notice:
                embed.add_field(name=f'{row[1]}, {row[2]}', value=f'[{row[0]}]({row[3]})', inline=False)

            print(f'알림 설정한 서버들을 대상으로 새 대학공지사항 알림을 전송합니다.')
            for channel_id in channels:
                try:
                    channel = bot.get_channel(channel_id[0])
                    await channel.send(embed=embed)
                except Exception:
                    continue

        if len(new_affairs_notice) > 0:
            embed = discord.Embed(title="새 학사공지", color=0x00205B)
            for row in new_affairs_notice:
                embed.add_field(name=f'{row[1]}, {row[2]}', value=f'[{row[0]}]({row[3]})', inline=False)

            print(f'알림 설정한 서버들을 대상으로 새 학사공지 알림을 전송합니다.')
            for channel_id in channels:
                try:
                    channel = bot.get_channel(channel_id[0])
                    await channel.send(embed=embed)
                except Exception:
                    continue

        if len(new_scholarship_notice) > 0:
            embed = discord.Embed(title="새 장학공지", color=0x333F48)
            for row in new_scholarship_notice:
                embed.add_field(name=f'{row[1]}, {row[2]}', value=f'[{row[0]}]({row[3]})', inline=False)

            print(f'알림 설정한 서버들을 대상으로 새 장학공지 알림을 전송합니다.')
            for channel_id in channels:
                try:
                    channel = bot.get_channel(channel_id[0])
                    await channel.send(embed=embed)
                except Exception:
                    continue

    global status
    status = cycle(['명령어: /도움', f'{BOT_VERSION}', f'{len(bot.guilds)}개의 서버와 함께'])


@tasks.loop(time=food_notification_time)
async def food_notification():
    now = datetime.datetime.now()
    channels = server_bot_settings.get_channel(now.hour)
    if len(channels) > 0:
        print(f'{now}에 {now.hour}시 알림 설정한 서버들을 대상으로 알림을 전송합니다.')
        for channel_id in channels:
            try:
                channel = bot.get_channel(channel_id[0])
                await 테파(channel)
                await _2학(channel)
            except Exception:
                continue
    else:
        print(f'{now} 시점에 {now.hour}시 알림 설정한 서버가 없습니다.')


@tasks.loop(seconds=3)
async def change_status():
    await bot.change_presence(activity=discord.Game(next(status)))


bot.run(discord_bot_token)  # Insert Your Bot Token
