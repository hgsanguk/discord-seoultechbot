"""
봇의 작동 로그를 기록하기 위한 모듈입니다.
폴더의 최상단, `run.py`와 같은 위치의 디렉토리에 `seoultechbot_discord.log`에 로그가 기록됩니다.\n
30일마다 로그 파일이 새 파일로 갱신되며 이전 파일은 `seoultechbot_discord.log.%Y%m%d(갱신일)` 형식으로 저장됩니다.
"""
import logging
from logging.handlers import TimedRotatingFileHandler


def setup(level: str):
    """
    로깅 레벨을 설정하고 고정된 형식에 따른 로거를 리턴합니다.
    :param level: 로깅 레벨을 str 형식으로 받아 로깅 레벨을 설정합니다. `level='DEBUG'` 는 DEBUG로, 이외의 경우엔 INFO로 설정됩니다.
    :return: 파일 이름, 형식, 이름이 설정된 Logger 객체
    """
    # 클래스 첫 호출에 로그 파일 이름 지정
    filename = "seoultechbot_discord.log"
    formatter = logging.Formatter('[%(asctime)s][%(levelname)s] - [%(name)s] %(message)s')

    file_handler = TimedRotatingFileHandler(filename, encoding='utf-8', when='D', interval=30, backupCount=6)
    file_handler.setFormatter(formatter)
    file_handler.suffix = "%Y%m%d"

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    discord_logger = logging.getLogger('discord')
    discord_logger.addHandler(file_handler)
    discord_logger.addHandler(stream_handler)

    seoultechbot_logger = logging.getLogger('seoultechbot')
    seoultechbot_logger.addHandler(file_handler)
    seoultechbot_logger.addHandler(stream_handler)

    if level == "DEBUG" or level == "debug":
        logging_level = logging.DEBUG
    else:
        logging_level = logging.INFO

    discord_logger.setLevel(logging_level)
    seoultechbot_logger.setLevel(level)

    return seoultechbot_logger
