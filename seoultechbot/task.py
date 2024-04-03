from itertools import cycle

import discord
from discord.ext import commands, tasks

from seoultechbot import SeoulTechBot, Logger


class Task(commands.Cog):
    """
    봇의 Task를 관리하는 클래스입니다.
    """
    def __init__(self, bot):
        self.__bot = bot
        self.__logger = Logger.setup('seoultechbot.task')
        self.__logger.debug(f'{__name__} 모듈 초기화 완료')
        self.__status = cycle(['도움말: /도움', f'{SeoulTechBot.VERSION}', f'{len(self.__bot.guilds)}개의 서버와 함께'])

    async def cog_load(self):
        self.__logger.info('봇의 Task 시작')
        self.__loop_status.start()

    async def cog_unload(self):
        self.__logger.info('봇의 Task 종료')
        self.__loop_status.cancel()

    @tasks.loop(seconds=3)
    async def __loop_status(self):
        """
        Discord 내에서 표시되는 봇 상태 중 '게임 하는 중'에 표시하는 메세지를 3초 간격으로 순환 표시합니다.
        """
        await self.__bot.change_presence(activity=discord.Game(next(SeoulTechBot.status)))


async def setup(bot):
    await bot.add_cog(Task(bot))

