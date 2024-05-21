"""
Discord의 SeoulTechBot 프로젝트 패키지입니다.
"""
__title__ = 'seoultechbot'
__author__ = 'Sanguk Lee'
__license__ = 'GPL-3.0'
__version__ = '1.3'


# 오류 시 종료를 위한 라이브러리
import sys

# 날씨 검증을 위한 모듈
from datetime import datetime

# 로거 설정을 위한 모듈
import logging
from logging.handlers import TimedRotatingFileHandler

# 봇 상태 표시를 위한 모듈
from itertools import cycle

# Discord 상에서 봇의 작동을 위한 패키지
import discord
from discord.ext import commands
from sqlalchemy.ext.asyncio import AsyncSession

# 봇 초기화에 필요한 패키지
from seoultechbot import scrapper, model
from .config import Config


class SeoulTechBot(commands.Bot):
    """
    :class:`commands.Bot` 클래스를 상속받아 SeoulTechBot의 정보를 관리하고, 초기화하는 메서드를 포함한 클래스입니다.

    Attributes:
        __game_name (cycle): Discord 내에서 표시되는 봇 상태 중 '게임 하는 중'에 표시할 메세지 cycle 입니다.
        __enable_weather_command (bool): 날씨 활성화 여부를 체크하는 변수입니다.
        __db_session (AsyncSession): 데이터베이스의 Session입니다.
        __config (seoultechbot.Config): 봇의 환경 설정입니다.
    """

    @property
    def game_name(self) -> cycle:
        return self.__game_name

    @property
    def enable_weather_command(self) -> bool:
        return self.__enable_weather_command

    @property
    def db_session(self) -> AsyncSession:
        return self.__db_session

    @property
    def config(self) -> Config:
        return self.__config

    def __init__(self):
        """
        설정의 유효성을 확인하고 로거를 설정한 뒤, 봇을 실행합니다.
        """
        self.__db_session = None
        self.__config = Config()  # 봇의 설정
        self.__enable_weather_command = False  # 날씨 명령어 활성화 여부
        self.__game_name = cycle(['봇 시작 중...'])
        
        # 자원 절약을 위해 필수적인 Intents만 허용합니다.
        intents = discord.Intents.none()
        # 봇을 사용하는 서버 확인을 위한 Intents
        intents.guilds = True

        # 로거 레벨 설정
        self.__setup_logger()

        # 봇 정보 로그에 표시
        self.__logger.info(f"SEOULTECHBOT - DISCORD BOT FOR SEOULTECH")
        self.__logger.info(f"VERSION {__version__}, BOT MODE: {self.__config.program_level}")
        self.__logger.debug("디버그 모드가 활성화되었습니다.")

        # Bot 객체 생성
        super().__init__(command_prefix="%", intents=intents, help_command=None)

    async def setup_hook(self):
        """
        봇 실행 파일들을 초기화하고 봇의 명령어를 Discord 서버와 동기화 합니다.
        """
        # 입력한 정보 유효성 확인
        await self.__verify()

        # 데이터베이스 초기화 및 세션 획득
        self.__db_session = await model.init_db(self.__config)

        # Cog 초기화
        self.__game_name = cycle(['봇 초기화 중...'])
        self.__logger.info('봇 초기화 중...')
        await self.load_extension('seoultechbot.event')
        await self.load_extension('seoultechbot.command.util')
        if self.__enable_weather_command:
            await self.load_extension('seoultechbot.command.weather')

        # Discord 서버와 명령어 동기화
        # DEBUG 모드이고 봇 소유자가 특정 서버에서 디버그를 원할 경우, 특정 서버에서만 명령어 동기화 진행
        self.__logger.info('Discord 서버와 봇의 명령어를 동기화 중...')
        if self.__config.program_level == "DEBUG" and self.__config.debug_server_id is not None:
            debug_server = discord.Object(id=self.__config.debug_server_id)
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

        self.refresh_guilds_count()
        self.__logger.info(f'{self.user.name} 실행 완료, {len(self.guilds)}개의 서버에서 봇 이용 중')

    async def close(self):
        """
        DB Session을 닫고 봇을 안전하게 종료합니다.
        """
        await self.__db_session.close()
        await super().close()

    def __setup_logger(self):
        """
        로깅 레벨을 설정합니다. 최상단, `run.py` 와 같은 위치의 디렉토리에 `seoultechbot.log` 에 로그가 기록됩니다.
        30일마다 로그 파일이 새 파일로 갱신되며 이전 파일은 `seoultechbot.log.%Y%m%d(로그 시작일)` 형식으로 저장됩니다.
        """
        # 로그 파일 이름과 형식 지정
        filename = "data/logs/seoultechbot.log"
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

        # sqlalchemy의 로그를 함께 출력하도록 설정
        sqlalchemy_logger = logging.getLogger('sqlalchemy')
        sqlalchemy_logger.addHandler(file_handler)
        sqlalchemy_logger.addHandler(stream_handler)

        self.__logger = logging.getLogger('seoultechbot')
        self.__logger.addHandler(file_handler)
        self.__logger.addHandler(stream_handler)

        if self.__config.program_level == "DEBUG":
            logging_level = logging.DEBUG
        else:
            logging_level = logging.INFO

        discord_logger.setLevel(logging_level)
        sqlalchemy_logger.setLevel(logging_level)
        self.__logger.setLevel(logging_level)

    async def __verify(self):
        """
        API 토큰의 유효성을 확인하고, 토큰이 비어있거나 올바르지 않은 경우 봇의 일부 기능을 비활성화합니다.
        """
        # 스크랩하는 주기가 너무 짧을 경우(60초 미만) 경고
        if self.__config.scrap_period < 60:
            self.__logger.warning("스크랩 주기가 60초 미만입니다. 봇이 원활하게 작동하지 않거나, 학교 홈페이지가 봇의 스크래핑을 거부할 가능성이 있습니다.")

        # 날씨 토큰 확인
        if self.__config.weather_api_token:
            self.__logger.info('오픈 API 기상청 단기예보 조회서비스 토큰 (앞 10자리): ' + self.__config.weather_api_token[0:10])
            result = await scrapper.weather.fetch(datetime.now())
            if not result:
                self.__logger.error('오픈 API 기상청 단기예보 조회서비스 토큰 검증 실패. 봇의 날씨 기능이 비활성화 됩니다.')
            else:
                self.__logger.info('오픈 API 기상청 단기예보 조회서비스 토큰 검증 성공.')
                self.__enable_weather_command = True
        else:
            self.__logger.warning('오픈 API 기상청 단기예보 조회서비스 토큰을 입력하지 않았습니다. 봇의 날씨 기능이 비활성화 됩니다.')

    def refresh_guilds_count(self):
        """
        봇의 '게임 하는 중' 메세지에서 봇을 사용 중인 서버의 갯수를 갱신합니다.
        """
        self.__game_name = cycle(['도움말: /도움', f'v{__version__}', f'{len(self.guilds)}개의 서버와 함께'])
        self.__logger.debug(f'이용 중인 서버 갯수 갱신. {len(self.guilds)}개의 서버에서 봇 이용 중')
