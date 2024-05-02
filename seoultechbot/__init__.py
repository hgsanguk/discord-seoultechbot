"""
Discord의 SeoulTechBot 프로젝트 패키지입니다.
"""
import asyncio
# 환경 변수 사용을 위한 모듈
import os

# 로거 설정을 위한 모듈
import logging
from datetime import datetime
from logging.handlers import TimedRotatingFileHandler

# 봇 상태 표시를 위한 모듈
from itertools import cycle

# Discord 상에서 봇의 작동을 위한 패키지
import discord
from discord.ext import commands

# OpenAPI 토큰 검증을 위한 패키지
from seoultechbot import scrapper


class SeoulTechBot(commands.Bot):
    """
    :class:`commands.Bot` 클래스를 상속받아 봇의 정보를 관리하고, 초기화하는 클래스입니다.

    Attributes:
        status (cycle): Discord 내에서 표시되는 봇 상태 중 '게임 하는 중'에 표시할 메세지 cycle 입니다.
        __VERSION (str): Discord의 SeoulTechBot 프로젝트 버전입니다.
        __program_level (str): 프로그램 레벨입니다. 기본은 'RELEASE'이며 'DEBUG'일 경우 디버그 모드로 작동합니다.
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
        self.__weather_api_token = os.getenv("STBOT_WEATHER_API_TOKEN")
        self.__scrap_period = os.getenv("STBOT_SCRAP_PERIOD", 600)
        self.__debug_server_id = os.getenv("STBOT_DEBUG_SERVER_ID", None)
        self.__valid_weather_api_token = False
        
        # 자원 절약을 위해 필수적인 Intents만 허용합니다.
        intents = discord.Intents.none()
        # 봇을 사용하는 서버 확인을 위한 Intents
        intents.guilds = True

        # 로거 레벨 설정
        self.__setup_logger()

        # 봇 정보 로그에 표시
        self.__logger.info(f"SEOULTECHBOT PROJECT - DISCORD BOT FOR SEOULTECH")
        self.__logger.info(f"PROJECT VERSION {SeoulTechBot.__VERSION}, BOT MODE: {self.__program_level}")
        self.__logger.debug("디버그 모드가 활성화되었습니다.")

        # 입력한 정보 유효성 확인
        self.__verify()

        # Bot 객체 생성
        super().__init__(command_prefix="%", intents=intents, help_command=None)

    async def setup_hook(self):
        """
        봇 실행 파일들을 초기화하고 봇의 명령어를 Discord 서버와 동기화 합니다.
        """
        # Cog 초기화
        SeoulTechBot.status = cycle(['봇 초기화 중...'])
        self.__logger.info('봇 초기화 중...')
        await self.load_extension('seoultechbot.event')
        await self.load_extension('seoultechbot.command.util')
        if self.__valid_weather_api_token:
            await self.load_extension('seoultechbot.command.weather')

        # Discord 서버와 명령어 동기화
        # DEBUG 모드이고 봇 소유자가 특정 서버에서 디버그를 원할 경우, 특정 서버에서만 명령어 동기화 진행
        self.__logger.info('Discord 서버와 봇의 명령어를 동기화 중...')
        if self.__program_level == "DEBUG" and self.__debug_server_id is not None:
            debug_server = discord.Object(id=self.__debug_server_id)
            self.tree.copy_global_to(guild=debug_server)
            synced = await self.tree.sync(guild=debug_server)
        else:
            synced = await self.tree.sync()
        self.__logger.debug(f'동기화된 명령어: {synced}')
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

    def __setup_logger(self):
        """
        로깅 레벨을 설정합니다. 최상단, `run.py` 와 같은 위치의 디렉토리에 `seoultechbot-discord.log` 에 로그가 기록됩니다.
        30일마다 로그 파일이 새 파일로 갱신되며 이전 파일은 `seoultechbot-discord.log.%Y%m%d(갱신일)` 형식으로 저장됩니다.
        """
        # 로그 파일 이름과 형식 지정
        filename = "seoultechbot-discord.log"
        formatter = logging.Formatter('[%(asctime)s][%(levelname)s] - [%(name)s] %(message)s')

        # 30일 간 6개의 로그, 총 180일 간의 로그를 저장
        file_handler = TimedRotatingFileHandler(filename, 'D', 30, 6, 'utf-8')
        file_handler.setFormatter(formatter)
        file_handler.suffix = "%Y%m%d"

        # 디버깅을 위해 콘솔 창에서도 로그를 출력하도록 설정
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)

        # discord.py의 로그를 함께 출력하도록 설정
        discord_logger = logging.getLogger('discord')
        discord_logger.addHandler(file_handler)
        discord_logger.addHandler(stream_handler)

        self.__logger = logging.getLogger('seoultechbot')
        self.__logger.addHandler(file_handler)
        self.__logger.addHandler(stream_handler)

        if self.__program_level == "DEBUG" or self.__program_level == "debug":
            logging_level = logging.DEBUG
        else:
            logging_level = logging.INFO

        discord_logger.setLevel(logging_level)
        self.__logger.setLevel(logging_level)

    def __verify(self):
        """
        API 토큰의 유효성을 확인하고, 토큰이 비어있거나 올바르지 않은 경우 봇의 일부 기능을 비활성화합니다.
        """
        # 스크랩하는 주기가 너무 짧을 경우(60초 미만) 경고
        if self.__scrap_period < 60:
            self.__logger.warning("스크랩 주기가 60초 미만입니다. 봇이 원활하게 작동하지 않거나, 학교 홈페이지가 봇의 스크래핑을 거부할 가능성이 있습니다.")

        # 날씨 토큰 확인
        if self.__weather_api_token:
            self.__logger.info('오픈 API 기상청 단기예보 조회서비스 토큰 (앞 10자리): ' + self.__weather_api_token[0:10])
            if not asyncio.run(scrapper.weather.fetch(datetime.now())):
                self.__logger.error('오픈 API 기상청 단기예보 조회서비스 토큰 검증 실패. 봇의 날씨 기능이 비활성화 됩니다.')
            else:
                self.__logger.info('오픈 API 기상청 단기예보 조회서비스 토큰 검증 성공.')
                self.__valid_weather_api_token = True
        else:
            self.__logger.warning('오픈 API 기상청 단기예보 조회서비스 토큰을 입력하지 않았습니다. 봇의 날씨 기능이 비활성화 됩니다.')
