# Built-in 라이브러리
from itertools import cycle

# discord.py 라이브러리
import discord
from discord import app_commands
from discord.ext import tasks

# 자체 라이브러리
import seoultechbot

bot = discord.Client(intents=discord.Intents.all())
tree = app_commands.CommandTree(bot)

# 봇 첫 실행시 첫 이벤트
@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online)
    await tree.sync()
    seoultechbot.logger.info('봇 실행 완료.')


@tasks.loop(seconds=3)
async def change_status():
    seoultechbot.status = cycle(['도움말: /도움', f'{seoultechbot.VERSION}', f'{len(bot.guilds)}개의 서버와 함께'])
    await bot.change_presence(activity=discord.Game(next(seoultechbot.status)))


if __name__ == "__main__":
    bot.run(seoultechbot.DISCORD_BOT_TOKEN)