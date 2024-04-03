"""
Discord의 SeoulTechBot 프로젝트 패키지입니다.
"""

# 환경 변수 사용을 위한 모듈
import os

# 에러 메세지 출력 및 종료를 위한 모듈
import sys

# 봇 상태 표시를 위한 모듈
from itertools import cycle

# Discord 상에서 봇의 작동을 위한 라이브러리
import discord
from discord.ext import commands

# 로그 생성을 위한 모듈
from .logger import Logger


class SeoulTechBot(commands.Bot):
    """
    :class:`commands.Bot` 클래스를 상속받아 봇의 정보를 관리하고, 초기화하는 클래스입니다.

    Attributes:
        VERSION (str): Discord의 SeoulTechBot 프로젝트 버전입니다.
        DISCORD_BOT_TOKEN (str): Discord Bot의 토큰입니다.
        WEATHER_API_TOKEN (str): 오픈 API 기상청 단기예보 조회서비스 토큰입니다.
        DEBUG_SERVER_ID (str): 디버깅 할 봇 소유자 서버의 ID입니다.
        PROGRAM_LEVEL (str): 프로그램 레벨입니다. 기본은 'RELEASE'이며 'DEBUG'일 경우 디버그 모드로 작동합니다.
        SCRAP_PERIOD (int): 대학교 공지사항을 스크래핑할 주기입니다. 단위는 초 단위이며, 단과대/학과 공지사항 스크래핑은 별도의 주기를 따릅니다.
        DB_TYPE (str): 봇이 사용할 DBMS 종류입니다. 현재 SQLite, MySQL/MariaDB를 지원하고 있습니다.
        status (cycle): Discord 내에서 표시되는 봇 상태 중 '게임 하는 중'에 표시할 메세지 cycle 입니다.
    """

    VERSION = 'v1.3'
    DISCORD_BOT_TOKEN = os.getenv("STBOT_DISCORD_BOT_TOKEN")
    WEATHER_API_TOKEN = os.getenv("STBOT_WEATHER_API_TOKEN")
    DEBUG_SERVER_ID = os.getenv("STBOT_DEBUG_SERVER_ID", None)
    PROGRAM_LEVEL = os.getenv("STBOT_PROGRAM_LEVEL", "RELEASE")
    SCRAP_PERIOD = os.getenv("STBOT_SCRAP_PERIOD", 600)
    DB_TYPE = os.getenv("STBOT_DB_TYPE", "SQLITE")

    status = cycle(['봇 시작 중...'])
    __logger = None

    def __init__(self):
        """
        봇 설정의 유효성을 확인하고 로거를 설정한 뒤 Bot 객체를 생성합니다.
        """
        # 자원 절약을 위해 필수적인 Intents만 허용합니다.
        intents = discord.Intents.none()
        # 봇을 사용하는 서버 확인을 위한 Intents
        intents.guilds = True

        # 로거의 레벨을 설정합니다.
        Logger.set_level(SeoulTechBot.PROGRAM_LEVEL)
        SeoulTechBot.__logger = Logger.setup('seoultechbot')

        # 봇 정보 로그에 표시
        SeoulTechBot.__logger.info(f"SEOULTECHBOT PROJECT with Discord")
        SeoulTechBot.__logger.info(f"Project Version {SeoulTechBot.VERSION}, BOT MODE: {SeoulTechBot.PROGRAM_LEVEL}")
        SeoulTechBot.__logger.debug("디버그 모드가 활성화되었습니다.")

        # 스크랩하는 주기가 너무 짧을 경우 경고
        if SeoulTechBot.SCRAP_PERIOD < 60:
            SeoulTechBot.__logger.warning("스크랩 주기가 60초 미만입니다. 봇이 원활하게 작동하지 않거나, 학교 홈페이지가 봇의 스크래핑을 거부할 가능성이 있습니다.")

        # 봇 토큰 확인
        if not SeoulTechBot.DISCORD_BOT_TOKEN:
            msg = '디스코드 봇 토큰을 입력하지 않았습니다. 토큰을 입력한 후 다시 시도해주세요.'
            SeoulTechBot.__logger.critical(msg)
            sys.exit(msg)
        else:
            SeoulTechBot.__logger.info('Discord 봇 토큰 (앞 10자리): ' + SeoulTechBot.DISCORD_BOT_TOKEN[0:10])

        # 날씨 토큰 확인

        if not SeoulTechBot.WEATHER_API_TOKEN:
            SeoulTechBot.__logger.warning('오픈 API 기상청 단기예보 조회서비스 토큰을 입력하지 않았습니다. 봇의 날씨 기능이 비활성화 됩니다.')
        else:
            SeoulTechBot.__logger.info('오픈 API 기상청 단기예보 조회서비스 토큰 (앞 10자리): ' + SeoulTechBot.WEATHER_API_TOKEN[0:10])

        # Bot 인스턴스 생성
        super().__init__(command_prefix="/", intents=intents, help_command=None)

    async def on_ready(self):
        """
        봇 시작 시 봇 실행 파일들을 초기화합니다.
        """
        SeoulTechBot.status = cycle(['봇 초기화 중...'])
        SeoulTechBot.__logger.info('봇 초기화 중...')
        await self.load_extension('seoultechbot.command.util')
        await self.load_extension('seoultechbot.event')
        await self.load_extension('seoultechbot.task')

        # SeoulTechBot.__logger.info('봇의 명령어를 Discord 서버와 동기화 중...')
        synced = await self.tree.sync(guild=discord.Object(id=SeoulTechBot.DEBUG_SERVER_ID) if SeoulTechBot.PROGRAM_LEVEL == "DEBUG" else None)
        self.__logger.debug(f'동기화된 명령어: {synced}')
        SeoulTechBot.status = cycle(['도움말: /도움', f'{SeoulTechBot.VERSION}', f'{len(self.guilds)}개의 서버와 함께'])
        SeoulTechBot.__logger.info(f'{self.user.name} 시작 완료, {len(self.guilds)}개의 서버에서 봇 이용 중')


def run():
    """
    봇을 시작하는 함수입니다. 별도의 Parameter는 없으며, 환경 변수에서 자동으로 Discord의 봇 토큰을 가져옵니다.
    """
    SeoulTechBot().run(SeoulTechBot.DISCORD_BOT_TOKEN, log_handler=None)