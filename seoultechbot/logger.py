import logging
from logging.handlers import TimedRotatingFileHandler


class Logger:
    """
    봇의 작동 로그를 기록하기 위한 클래스입니다.
    폴더의 최상단, `run.py`와 같은 위치의 디렉토리에 `seoultechbot_discord.log`에 로그가 기록됩니다.\n
    30일마다 로그 파일이 새 파일로 갱신되며 이전 파일은 `seoultechbot_discord.log.%Y%m%d(갱신일)` 형식으로 저장됩니다.
    """

    # 클래스 첫 호출에 로그 파일 이름 지정
    __filename = "seoultechbot_discord.log"
    __level = logging.INFO
    __formatter = logging.Formatter('[%(asctime)s][%(levelname)s] - [%(name)s] %(message)s')

    __file_handler = TimedRotatingFileHandler(__filename, encoding='utf-8', when='D', interval=30, backupCount=6)
    __file_handler.setFormatter(__formatter)
    __file_handler.suffix = "%Y%m%d"

    __stream_handler = logging.StreamHandler()
    __stream_handler.setFormatter(__formatter)

    __discord = logging.getLogger('discord')
    __discord.addHandler(__file_handler)
    __discord.addHandler(__stream_handler)

    @staticmethod
    def set_level(level: str):
        """
        로깅 레벨을 설정합니다.
        :param level: 로깅 레벨을 str 형식으로 받아 로깅 레벨을 설정합니다. `level='DEBUG'` 는 DEBUG로, 이외의 경우엔 INFO로 설정됩니다.
        :return:
        """
        Logger.__discord.setLevel(level)

        # 상황에 맞춰서 로깅 레벨을 조절
        if level == "DEBUG" or level == "debug":
            Logger.__level = logging.DEBUG
        else:
            Logger.__level = logging.INFO

    # 로거 설정 및 반환
    @staticmethod
    def setup(name: str) -> logging.Logger:
        """
        고정된 형식에 따른 logger를 return하는 method입니다.

        :param name: logger의 이름을 설정할 수 있습니다. 이 이름으로 봇의 어떤 부분이 로깅됐는지 확인할 수 있습니다.
        :return: 파일 이름, 형식, 이름이 설정된 Logger 객체
        """
        logger = logging.getLogger(name)
        logger.setLevel(Logger.__level)
        logger.addHandler(Logger.__file_handler)
        logger.addHandler(Logger.__stream_handler)

        return logger
