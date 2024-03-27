import logging
from datetime import datetime


class Logger:
    # 클래스 첫 호출에 로그 파일 이름 지정
    filename = "seoultechbot_discord_" + datetime.now().strftime("%Y%m%d-%H%M%S") + ".log"

    def __init__(self, level=logging.INFO):
        # 로그 레벨 지정(기본: INFO)
        if level == "DEBUG":
            self.level = logging.DEBUG
        else:
            self.level = logging.INFO

        self.formatter = logging.Formatter('[%(asctime)s][%(name)s] - [%(levelname)s] %(message)s')
        self.handler = logging.FileHandler(self.filename, encoding='utf-8')
        self.handler.setFormatter(self.formatter)

    # 로거 설정 및 반환
    def setup(self, name):
        logger = logging.getLogger(name)
        logger.setLevel(self.level)
        logger.addHandler(self.handler)

        return logger
