from datetime import datetime
import discord
from discord.ext import commands
import os
import menucrawler

game = discord.Game('명령어: /도움')
app = commands.Bot(command_prefix='/', intents=discord.Intents.all())


@app.event
async def on_ready():
    print('Done')
    await app.change_presence(status=discord.Status.online, activity=game)


@app.command(name="2학")
async def _2학(ctx):
    crawler_result = menucrawler.student_cafeteria_2()
    embed = discord.Embed(title="제2학생회관", description=datetime.today().strftime("%m월 %d일 식단표"))
    embed.add_field(name=f"{crawler_result[0][0]} `{crawler_result[0][1]}`", value=f"{crawler_result[0][2]}", inline=False)
    embed.add_field(name=f"{crawler_result[1][0]} `{crawler_result[1][1]}`", value=f"{crawler_result[1][2]}", inline=False)
    await ctx.send(embed=embed)


@app.command()
async def 테파(ctx):
    crawler_result = menucrawler.technopark()
    embed = discord.Embed(title="테크노파크", description=f"{crawler_result[0]}")
    embed.set_image(url=f"{crawler_result[1]}")
    await ctx.send(embed=embed)


@app.command()
async def 도움(ctx):
    embed = discord.Embed(title="봇 명령어 목록", description="`/2학`: 제2학생회관의 오늘 식단표를 출력합니다.\n`/테파`: 테크노파크의 이번 주 식단표를 출력합니다.")
    await ctx.send(embed=embed)

app.run(os.getenv('DiscordBotToken'))  # Insert Your Bot Token
