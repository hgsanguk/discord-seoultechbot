# 봇을 실행하게 될 파일
import discord
from discord import app_commands
from discord.ext import tasks

import json
import datetime

try:
    with open('../config.json') as f:
        config = json.load(f)
except FileNotFoundError:
    print("FileNotFoundError: config.json 파일이 없습니다.")
    print("프로그램 경로의 최상단에 있는 config_template.json를 참고하여 config.json 파일을 생성해주세요.")
    print("프로그램을 종료합니다.")
    exit(-1)

discord_bot_token = config["token"]["discord"]
weather_api_token = config["token"]["weather"]

print("Discord Bot Token: ", discord_bot_token[0:10])
print("오픈 API 기상청 단기예보 조회서비스 Token: ", weather_api_token[0:10])

bot = discord.Client(intents=discord.Intents.all())
tree = app_commands.CommandTree(bot)

global status
CRAWLING_PERIOD = 1
BOT_VERSION = 'v1.3'

food_notification_time = [datetime.time(hour=i, minute=0,
                                        tzinfo=datetime.timezone(datetime.timedelta(hours=9))) for i in range(9, 13)]
notice_crawling_time = [datetime.time(hour=i, minute=30,
                                      tzinfo=datetime.timezone(datetime.timedelta(hours=9))) for i in range(0, 24, CRAWLING_PERIOD)]
food_crawling_time = [datetime.time(hour=i, minute=0,
                                    tzinfo=datetime.timezone(datetime.timedelta(hours=9))) for i in range(0, 24, CRAWLING_PERIOD)]


@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online)
    await tree.sync()
    print(f'{datetime.datetime.now()}: 봇 실행 완료')

@tasks.loop(seconds=3)
async def change_status():
    await bot.change_presence(activity=discord.Game(next(status)))


bot.run(discord_bot_token)