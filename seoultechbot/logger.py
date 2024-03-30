import logging
from datetime import datetime


class Logger:
    # 클래스 첫 호출에 로그 파일 이름 지정
    filename = "seoultechbot_discord_" + datetime.now().strftime("%Y%m%d-%H%M%S") + ".log"
    level = None
    formatter = logging.Formatter('[%(asctime)s][%(name)s] - [%(levelname)s] %(message)s')
    handler = logging.FileHandler(filename, encoding='utf-8')
    handler.setFormatter(formatter)

    @staticmethod
    def set_level(level):
        if level == "DEBUG":
            Logger.level = logging.DEBUG
        else:
            Logger.level = logging.INFO

    # 로거 설정 및 반환
    @staticmethod
    def setup(name):
        logger = logging.getLogger(name)
        logger.setLevel(Logger.level)
        logger.addHandler(Logger.handler)

        return logger
