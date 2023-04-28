import json
import os

import discord
from discord import app_commands
from discord.ext import tasks, commands

from seoultechbot.crawler import Food
import seoultechbot.db
import seoultechbot.settings

try:
    json_path = os.path.dirname(os.path.abspath(__file__)) + "/seoultechbot.json"
    with open(json_path, "r") as json_file:
        json_data = json.load(json_file)
        discord_bot_token = json_data['config']['discord_token']
        weather_api_token = json_data['config']['weather_openapi_token']
        crawling_period = json_data['config']['crawling_period']

    if (len(crawling_period) == 0 or len(weather_api_token) == 0):
        raise KeyError
    crawling_period = int(crawling_period)
    print("Discord Bot 토큰: ", discord_bot_token)
    print("오픈 API 기상청 단기예보 조회서비스 토큰: ", weather_api_token)
except FileNotFoundError:
    # json 파일 생성 후 종료
    print("seoultechbot.json 파일을 찾을 수 없습니다. json 파일을 작성 후 다시 실행해주세요.")
    exit()
except KeyError:
    print("json 파일이 완성되지 않았습니다. json 파일을 확인 후 실행해주세요.")

# bot = discord.Client(intents=discord.Intents.all())
# tree = app_commands.CommandTree(bot)

# class Main(commands.Cog):
#     def __init__(self, bot: commands.Bot) -> None:
#         self.bot = bot

    
# async def setup(bot: commands.Bot) -> None:
#     await bot.add_cog(Main(bot))
#     await bot.add_cog(Food(bot))