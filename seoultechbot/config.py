import os


class Config:
    """
    봇의 환경설정을 담은 싱글톤 클래스입니다.

    Attributes:
        __program_level: 프로그램 레벨입니다. 기본은 'RELEASE'이며 'DEBUG'일 경우 디버그 모드로 작동합니다.
        __weather_api_token: 공공데이터포털 오픈 API 기상청 단기예보 조회서비스 토큰입니다.
        __scrap_period: 대학교 공지사항을 스크래핑할 주기입니다. 단위는 초 단위이며, 단과대/학과 공지사항 스크래핑은 별도의 주기를 따릅니다.
        __debug_server_id: 디버깅 할 봇 서버의 ID입니다. 입력하지 않을 경우 명령어를 전체 서버와 동기화하므로 디버깅에 시간이 소요될 수 있습니다.
        __db_connection_str: 데이터베이스의 Connection String 입니다.
    """
    __instance = None

    def __new__(cls):
        if not cls.__instance:
            cls.__instance = super(Config, cls).__new__(cls)
        return cls.__instance

    def __init__(self):
        self.__program_level: str = os.getenv("STBOT_PROGRAM_LEVEL", "RELEASE")
        self.__weather_api_token = os.getenv("STBOT_WEATHER_API_TOKEN")
        self.__scrap_period = os.getenv("STBOT_SCRAP_PERIOD", 600)
        self.__debug_server_id = os.getenv("STBOT_DEBUG_SERVER_ID", None)

        self.__db_type = os.getenv("STBOT_DB_TYPE", "SQLITE")
        self.__db_host = os.getenv("STBOT_DB_HOST")
        self.__db_port = os.getenv("STBOT_DB_PORT", 3306)
        self.__db_name = os.getenv("STBOT_DB_NAME", "seoultechbot")
        self.__db_user = os.getenv("STBOT_DB_USER")
        self.__db_password = os.getenv("STBOT_DB_PASSWORD")

        # DB 유형에 따라 Connection String 설정
        if self.__db_type == "MYSQL" or self.__db_type == "MARIADB":
            self.__db_connection_str = f"mysql+aiomysql://{self.__db_user}:{self.__db_password}@{self.__db_host}:{self.__db_port}/{self.__db_name}"
        else:
            self.__db_connection_str = f"sqlite+aiosqlite:///data/db/{self.__db_name}.db"

    @property
    def program_level(self):
        return self.__program_level

    @property
    def weather_api_token(self):
        return self.__weather_api_token

    @property
    def scrap_period(self):
        return self.__scrap_period

    @property
    def debug_server_id(self):
        return self.__debug_server_id

    @property
    def db_connection_str(self):
        return self.__db_connection_str
