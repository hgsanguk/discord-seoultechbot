"""
Discord의 SeoulTechBot 프로젝트 패키지입니다.
"""

# 환경 변수 사용을 위한 모듈
import os

# 에러 메세지 출력 및 종료를 위한 모듈
import sys

# 봇 상태 표시를 위한 모듈
from itertools import cycle

# Discord 상에서 봇의 작동을 위한 패키지
import discord
from discord.ext import commands

# 로그 생성을 위한 모듈
import seoultechbot.logger


class SeoulTechBot(commands.Bot):
    """
    :class:`commands.Bot` 클래스를 상속받아 봇의 정보를 관리하고, 초기화하는 클래스입니다.

    Attributes:
        status (cycle): Discord 내에서 표시되는 봇 상태 중 '게임 하는 중'에 표시할 메세지 cycle 입니다.
        __VERSION (str): Discord의 SeoulTechBot 프로젝트 버전입니다.
        __program_level (str): 프로그램 레벨입니다. 기본은 'RELEASE'이며 'DEBUG'일 경우 디버그 모드로 작동합니다.
        __discord_bot_token (str): Discord Bot의 토큰입니다.
        __weather_api_token (str): 오픈 API 기상청 단기예보 조회서비스 토큰입니다.
        __scrap_period (int): 대학교 공지사항을 스크래핑할 주기입니다. 단위는 초 단위이며, 단과대/학과 공지사항 스크래핑은 별도의 주기를 따릅니다.
        __debug_server_id (str): 디버깅 할 봇 서버의 ID입니다. 입력하지 않을 경우 명령어를 전체 서버와 동기화하므로 디버깅에 시간이 소요될 수 있습니다.
        __logger (logging.logger): 프로젝트 내 모든 로거의 부모 로거입니다.
    """

    status = cycle(['봇 시작 중...'])
    __VERSION = 'v1.3'

    @staticmethod
    def get_version() -> str:
        """
        프로젝트의 버전을 가져옵니다.
        """
        return SeoulTechBot.__VERSION

    def __init__(self):
        """
        설정의 유효성을 확인하고 로거를 설정한 뒤, 봇을 실행합니다.
        """
        self.__program_level = os.getenv("STBOT_PROGRAM_LEVEL", "RELEASE")
        self.__discord_bot_token = os.getenv("STBOT_DISCORD_BOT_TOKEN")
        self.__weather_api_token = os.getenv("STBOT_WEATHER_API_TOKEN")
        self.__scrap_period = os.getenv("STBOT_SCRAP_PERIOD", 600)
        self.__debug_server_id = os.getenv("STBOT_DEBUG_SERVER_ID", None)
        self.____logger = None
        
        # 자원 절약을 위해 필수적인 Intents만 허용합니다.
        intents = discord.Intents.none()
        # 봇을 사용하는 서버 확인을 위한 Intents
        intents.guilds = True

        # 로거 레벨 설정
        self.__logger = logger.setup(self.__program_level)

        # 봇 정보 로그에 표시
        self.__logger.info(f"SEOULTECHBOT PROJECT - DISCORD BOT FOR SEOULTECH")
        self.__logger.info(f"PROJECT VERSION {SeoulTechBot.__VERSION}, BOT MODE: {self.__program_level}")
        self.__logger.debug("디버그 모드가 활성화되었습니다.")

        # 스크랩하는 주기가 너무 짧을 경우(60초 미만) 경고
        if self.__scrap_period < 60:
            self.__logger.warning("스크랩 주기가 60초 미만입니다. 봇이 원활하게 작동하지 않거나, 학교 홈페이지가 봇의 스크래핑을 거부할 가능성이 있습니다.")

        # 봇 토큰 확인
        if not self.__discord_bot_token:
            msg = '디스코드 봇 토큰을 입력하지 않았습니다. 토큰을 입력한 후 다시 시도해주세요.'
            self.__logger.critical(msg)
            sys.exit(msg)
        else:
            self.__logger.info('Discord 봇 토큰 (앞 10자리): ' + self.__discord_bot_token[0:10])

        # 날씨 토큰 확인
        if not self.__weather_api_token:
            self.__logger.warning('오픈 API 기상청 단기예보 조회서비스 토큰을 입력하지 않았습니다. 봇의 날씨 기능이 비활성화 됩니다.')
        else:
            self.__logger.info('오픈 API 기상청 단기예보 조회서비스 토큰 (앞 10자리): ' + self.__weather_api_token[0:10])

        # Bot 객체 생성
        super().__init__(command_prefix="%", intents=intents, help_command=None)

        # 봇 시작
        self.run(self.__discord_bot_token, log_handler=None)

    async def setup_hook(self):
        """
        봇 실행 파일들을 초기화하고 봇의 명령어를 Discord 서버와 동기화 합니다.
        """
        # Cog 초기화
        SeoulTechBot.status = cycle(['봇 초기화 중...'])
        self.__logger.info('봇 초기화 중...')
        await self.load_extension('seoultechbot.command.util')
        await self.load_extension('seoultechbot.event')

        # Discord 서버와 명령어 동기화
        # DEBUG 모드이고 봇 소유자가 특정 서버에서 디버그를 원할 경우, 특정 서버에서만 명령어 동기화 진행
        self.__logger.info('Discord 서버와 봇의 명령어를 동기화 중...')
        if self.__program_level == "DEBUG" and self.__debug_server_id is not None:
            debug_server = discord.Object(id=self.__debug_server_id)
            self.tree.copy_global_to(guild=debug_server)
            synced = await self.tree.sync(guild=debug_server)
        else:
            synced = await self.tree.sync()
        self.____logger.debug(f'동기화된 명령어: {synced}')
        if len(synced) > 0:
            self.__logger.info('Discord 서버와 봇의 명령어 동기화 완료')
        else:
            self.__logger.error('Discord 서버와 봇의 명령어 동기화 실패')

    async def on_ready(self):
        """
        봇 Task를 초기화하고 실행 과정을 마무리 합니다.
        """
        await self.load_extension('seoultechbot.task')

        SeoulTechBot.status = cycle(['도움말: /도움', f'{SeoulTechBot.__VERSION}', f'{len(self.guilds)}개의 서버와 함께'])
        self.__logger.info(f'{self.user.name} 실행 완료, {len(self.guilds)}개의 서버에서 봇 이용 중')
