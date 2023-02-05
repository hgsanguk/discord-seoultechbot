# Built-in & discord.py Library
import datetime
import os
from itertools import cycle
import discord
from discord import app_commands
from discord.ext import tasks

# TechBot Library
import server_bot_settings
import menucrawler
import noticecrawler
import weather

token_path = os.path.dirname(os.path.abspath(__file__)) + "/token"
token_file = open(token_path, "r", encoding="utf-8").read().split()
discord_bot_token = token_file[0]
weather_api_token = token_file[1]

print("Discord Bot Token: ", discord_bot_token)
print("오픈 API 기상청 단기예보 조회서비스 Token: ", weather_api_token)

bot = discord.Client(intents=discord.Intents.all())
tree = app_commands.CommandTree(bot)
global status
CRAWLING_PERIOD = 1
BOT_VERSION = 'v1.2.1'
food_notification_time = [datetime.time(hour=i, minute=0,
                                        tzinfo=datetime.timezone(datetime.timedelta(hours=9))) for i in range(9, 13)]
notice_crawling_time = [datetime.time(hour=i, minute=30,
                                      tzinfo=datetime.timezone(datetime.timedelta(hours=9))) for i in range(0, 24, CRAWLING_PERIOD)]
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
    schedule_notification.start()
    change_status.start()

    # 봇 상태 표시
    global status
    status = cycle(['도움말: /도움', f'{BOT_VERSION}', f'{len(bot.guilds)}개의 서버와 함께'])

    # 알림을 한꺼번에 보내지 않도록 미리 알림을 크롤링해서 DB로 담음
    noticecrawler.get_notice('notice', 'University')
    noticecrawler.get_notice('matters', 'Affairs')
    noticecrawler.get_notice('janghak', 'Scholarship')
    noticecrawler.get_domi_notice()

    # 오늘의 식단을 크롤링
    await food_crawling()
    await bot.change_presence(status=discord.Status.online)
    await tree.sync()
    print(f'{datetime.datetime.now()}: 봇 실행 완료')


@bot.event
async def on_guild_join(guild):
    for channel in guild.text_channels:
        if channel.permissions_for(guild.me).send_messages:
            await channel.send(':wave: 안녕하세요! 서울과학기술대학교 비공식 디스코드 봇, 테크봇을 이용해주셔서 감사합니다.\n'
                               '`/도움` 명령어로 명령어의 목록을 확인하실 수 있습니다.')
            break


# 여기서부터 봇 명령어 코드입니다.

@tree.command(name='2학', description='제2학생회관의 오늘 식단표를 보여줍니다. 옵션으로 내일의 식단표를 볼 수 있습니다.')
@app_commands.choices(날짜=[app_commands.Choice(name='내일', value=1)])
@app_commands.describe(날짜='보고 싶은 식단표의 날짜를 선택합니다.')
async def _2학(interaction, 날짜: app_commands.Choice[int] = 0):
    day = datetime.datetime.now()
    day_str = '오늘'
    try:
        if 날짜 != 0:
            day_str = '내일'
            day += datetime.timedelta(days=날짜.value)
            if day.weekday() >= 5:
                raise IndexError
            try:
                menucrawler.get_sc2_menu(int(day.strftime('%y%m%d')))
            except IndexError:
                menucrawler.student_cafeteria_2(tomorrow=True)
        date_str = '{today.month}월 {today.day}일 식단'.format(today=day)
        food_data = menucrawler.get_sc2_menu(int(day.strftime('%y%m%d')))
        embed = discord.Embed(title="제2학생회관", description=date_str, color=0x73BF1F)
        embed.add_field(name=f"점심: {food_data[0]} `{food_data[1]}`", value=f"{food_data[2]}", inline=False)
        if food_data[3] != '간단 snack':
            embed.add_field(name=f"점심: {food_data[3]} `{food_data[4]}`", value=f"{food_data[5]}", inline=False)
        embed.add_field(name=f"저녁: {food_data[6]} `{food_data[7]}`", value=f"{food_data[8]}", inline=False)
        await interaction.response.send_message(embed=embed)
    except IndexError:
        embed = discord.Embed(title="제2학생회관", description=day_str + ' 등록된 식단이 없습니다.', color=0x73BF1F)
        await interaction.response.send_message(embed=embed)


@tree.command(description='테크노파크의 이번 주 식단표를 보여줍니다.')
async def 테파(interaction):
    try:
        today = datetime.datetime.now()
        food_data = menucrawler.get_technopark_menu(int(today.strftime('%y%W')))
        embed = discord.Embed(title="테크노파크", description=f"{food_data[0]}", color=0x0950A1)
        embed.set_image(url=f"{food_data[1]}")
        await interaction.response.send_message(embed=embed)
    except IndexError:
        embed = discord.Embed(title="테크노파크", description='이번 주에 등록된 식단표가 없습니다.', color=0x0950A1)
        await interaction.response.send_message(embed=embed)


@tree.command(description='현재 캠퍼스의 날씨와 1 ~ 6시간 뒤 날씨 예보를 보여줍니다.')
async def 날씨(interaction):
    try:
        await interaction.response.defer()
        date = weather.get_weather(weather_api_token)[0]
        data = weather.get_weather(weather_api_token)[1]

        if 8 <= date.hour <= 16:
            color = 0x99CCFF
        elif 5 <= date.hour < 8:
            color = 0xFAEBD7
        elif 16 < date.hour < 19:
            color = 0xF29886
        else:
            color = 0x000080

        embed = discord.Embed(title="이 시간 캠퍼스 날씨",
                              description='{day.month}월 {day.day}일 {day.hour}시 {day.minute}분 공릉동의 날씨입니다.'
                              .format(day=date), color=color)
        string_1 = ':droplet: 습도: ' + data[0][5] + '%\n:dash: 바람: ' + data[0][7] + '(' + data[0][6] + '°) 방향으로 ' + data[0][8] + 'm/s'
        string_2 = ':cloud_snow: 강수량 :' + data[0][4] + '\n:thermometer: 기온: ' + data[0][0] + '°C'
        if data[0][3] == '1':
            embed.add_field(name=':umbrella: 비\n' + string_2, value=string_1, inline=False)
        elif data[0][3] == '2':
            embed.add_field(name=':umbrella: 눈비\n' + string_2, value=string_1, inline=False)
        elif data[0][3] == '3':
            embed.add_field(name=':snowman2: 눈\n' + string_2, value=string_1, inline=False)
        elif data[0][3] == '4':
            embed.add_field(name=':white_sun_rain_cloud: 소나기\n' + string_2, value=string_1, inline=False)
        elif data[0][3] == '5':
            embed.add_field(name=':sweat_drops: 빗방울\n' + string_2, value=string_1, inline=False)
        elif data[0][3] == '6':
            embed.add_field(name=':umbrella: 싸락눈/빗방울\n' + string_2, value=string_1, inline=False)
        elif data[0][3] == '7':
            embed.add_field(name=':snowflake: 싸락눈\n' + string_2, value=string_1, inline=False)
        else:
            embed.add_field(name=data[0][1] + ' ' + data[0][2] + '\n:thermometer: 기온: ' + data[0][0] + '°C', value=string_1, inline=False)

        result_str = ''
        for i in range(1, 6):
            time_str = '**' + data[i][9] + '시**: '
            temp_str = ' ' + data[i][0] + '°C, :droplet: ' + data[i][5] + '%\n'
            if data[i][3] == '1':
                result_str += time_str + ':umbrella:' + temp_str
            elif data[i][3] == '2':
                result_str += time_str + ':umbrella:/:snowman2:' + temp_str
            elif data[i][3] == '3':
                result_str += time_str + ':snowman2:' + temp_str
            elif data[i][3] == '4':
                result_str += time_str + ':white_sun_rain_cloud:' + temp_str
            elif data[i][3] == '5':
                result_str += time_str + ':sweat_drops:' + temp_str
            elif data[i][3] == '6':
                result_str += time_str + ':snowflake:/:umbrella:' + temp_str
            elif data[i][3] == '7':
                result_str += time_str + ':snowflake:' + temp_str
            else:
                result_str += time_str + data[i][1] + temp_str

        embed.add_field(name='날씨 예보', value=result_str, inline=False)
        embed.set_footer(text='기상청 초단기예보 조회 서비스 오픈 API를 이용한 것으로, 실제 기상상황과 차이가 있을 수 있습니다.')

        await interaction.followup.send(embed=embed)
    except weather.requests.exceptions.Timeout:
        await interaction.followup.send('날씨를 불러오는 중 문제가 발생했습니다. 다시 시도해주세요.')


@tree.command(description='테크봇의 명령어 목록과 설명을 보여줍니다.')
async def 도움(interaction):
    embed = discord.Embed(title="봇 명령어 목록", color=0x711E92)
    embed.add_field(name=':warning:주의사항:warning:', value='**봇 입장 후 `/알림설정` 명령어를 사용해야 학교 공지사항과 학사일정, 학식 알림을 받을 수 있습니다.**\n'
                                                         '학교 공지사항은 학교 홈페이지의 **대학공지사항, 학사공지, 장학공지, [선택]생활관공지**를 알려드립니다. '
                                                         '이외의 공지사항은 학교 홈페이지를 참고하시기 바랍니다.\n', inline=False)
    embed.add_field(name='`/2학 [날짜]`', value='제2학생회관의 오늘 식단을 보여줍니다. `[날짜]` 옵션으로 내일의 식단을 볼 수 있습니다.', inline=False)
    embed.add_field(name='`/테파`', value='테크노파크의 이번 주 식단표를 보여줍니다.', inline=False)
    embed.add_field(name='`/날씨`', value='현재 캠퍼스의 날씨와 1 ~ 6시간 뒤 날씨 예보를 보여줍니다.', inline=False)
    embed.add_field(name='`/핑`', value='명령어 입력 시점부터 메세지 전송까지 총 지연시간을 보여줍니다.', inline=False)
    embed.add_field(name='`/알림설정 [학식알림] [생활관공지알림]`', value='알림을 설정하는 명령어입니다. 해당 명령어를 입력한 채널이 각종 알림을 받을 채널이 됩니다. (해당 명령어의 사용자는 관리자 권한이 있어야 합니다.)', inline=False)
    await interaction.response.send_message(embed=embed)


@tree.command(description='명령어 입력 시점부터 메세지 전송까지 총 지연시간을 보여줍니다.')
async def 핑(interaction):
    embed = discord.Embed(title=':ping_pong: 퐁!', description=f'지연시간: {round(bot.latency * 1000)} ms', color=0x711E92)
    await interaction.response.send_message(embed=embed)


# 여기서부터 봇 설정 관련 명령어입니다.

@tree.command(description='(관리자) 알림을 설정하는 명령어입니다. 해당 명령어를 입력한 채널이 각종 알림을 받을 채널이 됩니다.')
@app_commands.choices(학식알림=[app_commands.Choice(name='받지 않음', value=0), app_commands.Choice(name='9시', value=9),
                                   app_commands.Choice(name='10시', value=10), app_commands.Choice(name='11시', value=11),
                                   app_commands.Choice(name='12시', value=12)])
@app_commands.describe(학식알림="선택한 시간대(9시 ~ 12시)에 학식 메뉴 알림을 받습니다. 학식 메뉴 알림이 필요없다면 '받지 않음'을 선택해주세요.")
@app_commands.choices(생활관공지알림=[app_commands.Choice(name='받지 않음', value=0), app_commands.Choice(name='받음', value=1)])
@app_commands.describe(생활관공지알림='생활관 공지 알림을 받을지 선택하는 옵션입니다.')
async def 알림설정(interaction, 학식알림: app_commands.Choice[int], 생활관공지알림: app_commands.Choice[int]):
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message(':no_entry: 해당 명령어를 실행할 권한이 없습니다.', ephemeral=True)
    else:
        arg1 = 학식알림.value
        arg2 = 생활관공지알림.value
        server_bot_settings.set_notification_channel(interaction.guild.id, interaction.channel.id, arg1)
        server_bot_settings.set_dormitory_notification(interaction.guild.id, arg2)

        embed = discord.Embed(title=f':white_check_mark: {interaction.guild.name}의 알림 설정 결과',
                              description=f'알림 받을 채널 이름: `{interaction.channel.name}`', color=0x711E92)

        setting_log = f'{datetime.datetime.now()}: {interaction.guild.name}({interaction.guild.id}) 서버의 {interaction.channel.name}({interaction.channel.id}) 채널에서 알림 받을 채널 설정.'
        if arg1 == 0:
            setting_log += ' 학식 알림 받지 않음.'
            embed.add_field(name='학식 알림', value='`받지 않음`')
        elif 9 <= arg1 <= 12:
            setting_log += f' 학식 알림 시간: {arg1}시.'
            embed.add_field(name='학식 알림', value=f'`{arg1}시 정각에 받음`')

        if arg2 == 1:
            setting_log += ' 기숙사 알림 켬.'
            embed.add_field(name='생활관 공지 알림', value='`받음`')
        else:
            setting_log += ' 기숙사 알림 끔.'
            embed.add_field(name='생활관 공지 알림', value='`받지 않음`')

        print(setting_log)
        await interaction.response.send_message(embed=embed)


# 여기서부터 봇의 자동화 작업 코드입니다.

@tasks.loop(time=food_crawling_time)
async def food_crawling():
    today = datetime.datetime.now()
    if today.weekday() < 5:
        try:
            menucrawler.get_sc2_menu(int(today.strftime('%y%m%d')))
        except IndexError:
            print(f'{today}: 제2학생회관 식단 크롤링 시도...')
            menucrawler.student_cafeteria_2()
        try:
            menucrawler.get_technopark_menu(int(today.strftime('%y%W')))
        except IndexError:
            print(f'{today}: 서울테크노파크 식단 크롤링 시도...')
            menucrawler.technopark()


@tasks.loop(time=notice_crawling_time)
async def notice_crawling():
    print(f'{datetime.datetime.now()}: 공지사항 크롤링 시도...')
    try:
        new_univ_notice = noticecrawler.get_notice('notice', 'University')
        new_affairs_notice = noticecrawler.get_notice('matters', 'Affairs')
        new_scholarship_notice = noticecrawler.get_notice('janghak', 'Scholarship')
        new_dormitory_notice = noticecrawler.get_domi_notice()
    except noticecrawler.requests.ConnectTimeout:
        new_univ_notice = []
        new_affairs_notice = []
        new_scholarship_notice = []
        new_dormitory_notice = []
        print(f'{datetime.datetime.now()}: 학교 홈페이지 연결 실패. 다음 주기에 다시 시도합니다.')

    univ_notice_embed = discord.Embed(title="새 대학공지사항", color=0xA4343A)
    scholarship_embed = discord.Embed(title="새 장학공지", color=0x333F48)
    affairs_embed = discord.Embed(title="새 학사공지", color=0x00205B)

    for row in new_univ_notice:
        univ_notice_embed.add_field(name=row[1], value=f'[{row[0]}]({row[2]})', inline=False)
    for row in new_affairs_notice:
        affairs_embed.add_field(name=row[1], value=f'[{row[0]}]({row[2]})', inline=False)
    for row in new_scholarship_notice:
        scholarship_embed.add_field(name=row[1], value=f'[{row[0]}]({row[2]})', inline=False)

    channels = server_bot_settings.get_channel_all()
    if len(new_univ_notice) > 0 or len(new_affairs_notice) > 0 or len(new_scholarship_notice) > 0:
        print(f'{datetime.datetime.now()}: 알림 설정한 서버들을 대상으로 새 공지사항 알림을 전송합니다.')
        for channel_id in channels:
            try:
                channel = bot.get_channel(channel_id[0])
                if len(new_univ_notice) > 0:
                    await channel.send(embed=univ_notice_embed)
                if len(new_affairs_notice) > 0:
                    await channel.send(embed=affairs_embed)
                if len(new_scholarship_notice) > 0:
                    await channel.send(embed=scholarship_embed)
            except Exception as e:
                print(f'{datetime.datetime.now()}: {channel_id[0]} 채널에 알림을 보낼 수 없습니다. 예외명: {e}')
                continue

    if len(new_dormitory_notice) > 0:
        embed = discord.Embed(title="새 생활관공지", color=0x007EE9)
        channels_domi = server_bot_settings.get_channel_dormitory()
        for row in new_dormitory_notice:
            embed.add_field(name=row[1], value=f'[{row[0]}]({row[2]})', inline=False)

        print(f'{datetime.datetime.now()}: 알림 설정한 서버들을 대상으로 새 생활관공지 알림을 전송합니다.')
        for channel_id in channels_domi:
            try:
                channel = bot.get_channel(channel_id[0])
                await channel.send(embed=embed)
            except Exception as e:
                print(f'{datetime.datetime.now()}: {channel_id[0]} 채널에 알림을 보낼 수 없습니다. 예외명: {e}')
                continue

    global status
    status = cycle(['도움말: /도움', f'{BOT_VERSION}', f'{len(bot.guilds)}개의 서버와 함께'])


@tasks.loop(time=food_notification_time)
async def food_notification():
    now = datetime.datetime.now()
    if now.weekday() < 5:
        channels = server_bot_settings.get_channel(now.hour)
        try:
            day_str = '{today.month}월 {today.day}일 식단표'.format(today=now)
            food_data = menucrawler.get_sc2_menu(int(now.strftime('%y%m%d')))
            sc2_embed = discord.Embed(title="제2학생회관", description=day_str, color=0x73BF1F)
            sc2_embed.add_field(name=f"점심: {food_data[0]} `{food_data[1]}`", value=f"{food_data[2]}", inline=False)
            if food_data[3] != '간단 snack':
                sc2_embed.add_field(name=f"점심: {food_data[3]} `{food_data[4]}`", value=f"{food_data[5]}", inline=False)
            sc2_embed.add_field(name=f"저녁: {food_data[6]} `{food_data[7]}`", value=f"{food_data[8]}", inline=False)
        except IndexError:
            sc2_embed = discord.Embed(title="제2학생회관", description='오늘 등록된 식단표가 없습니다.', color=0x73BF1F)

        try:
            food_data = menucrawler.get_technopark_menu(int(now.strftime('%y%W')))
            tp_embed = discord.Embed(title="테크노파크", description=food_data[0], color=0x0950A1)
            tp_embed.set_image(url=food_data[1])
        except IndexError:
            tp_embed = discord.Embed(title="테크노파크", description='이번 주에 등록된 식단표가 없습니다.', color=0x0950A1)

        if len(channels) > 0:
            print(f'{now}: {now.hour}시 알림 설정한 서버들을 대상으로 알림을 전송합니다.')
            for channel_id in channels:
                try:
                    channel = bot.get_channel(channel_id[0])
                    await channel.send(embed=sc2_embed)
                    await channel.send(embed=tp_embed)
                except Exception as e:
                    print(f'{datetime.datetime.now()}: {channel_id[0]} 채널에 알림을 보낼 수 없습니다. 예외명: {e}')
                    continue


@tasks.loop(time=datetime.time(hour=0, minute=0, tzinfo=datetime.timezone(datetime.timedelta(hours=9))))
async def schedule_notification():
    now = datetime.datetime.now()
    schedule = noticecrawler.get_univ_schedule()
    schedule_embed = discord.Embed(title='오늘의 일정', description='오늘 시작하거나 끝나는 학사일정입니다.', color=0x427EE2)
    channels = server_bot_settings.get_channel_all()
    if len(schedule) > 0:
        for row in schedule:
            if '\n\n' in row:
                task = row.split('\n\n')[0]
                date = row.split('\n\n')[1]
                schedule_embed.add_field(name=task, value=date, inline=False)
            else:
                schedule_embed.add_field(name=row, value=now.strftime('%Y.%m.%d'), inline=False)

        if len(channels) > 0:
            print(f'{now}: 알림 설정한 서버들을 대상으로 오늘의 학사일정 알림을 전송합니다.')
            for channel_id in channels:
                try:
                    channel = bot.get_channel(channel_id[0])
                    await channel.send(embed=schedule_embed)
                except Exception as e:
                    print(f'{datetime.datetime.now()}: {channel_id[0]} 채널에 알림을 보낼 수 없습니다. 예외명: {e}')
                    continue


@tasks.loop(seconds=3)
async def change_status():
    await bot.change_presence(activity=discord.Game(next(status)))


bot.run(discord_bot_token)
