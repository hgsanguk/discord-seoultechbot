import logging
from datetime import datetime


class Logger:
    """
    봇의 작동 로그를 기록하기 위한 클래스입니다.
    파일 이름과 형식은 지정되어 있으므로 초기화 과정 외의 런타임에서 변경하지 말 것을 권장합니다.
    """

    # 클래스 첫 호출에 로그 파일 이름 지정
    filename = "seoultechbot_discord_" + datetime.now().strftime("%Y%m%d-%H%M%S") + ".log"
    level = logging.INFO
    formatter = logging.Formatter('[%(asctime)s][%(name)s] - [%(levelname)s] %(message)s')
    handler = logging.FileHandler(filename, encoding='utf-8')
    handler.setFormatter(formatter)

    @staticmethod
    def set_level(level):
        """
        로깅 레벨을 설정합니다.
        :param level: 로깅 레벨을 str 형식으로 받아 로깅 레벨을 설정합니다. `level='DEBUG'` 는 DEBUG로, 이외의 경우엔 INFO로 설정됩니다.
        :return:
        """
        # 상황에 맞춰서 로깅 레벨을 조절
        if level == "DEBUG" or "debug":
            Logger.level = logging.DEBUG
        else:
            Logger.level = logging.INFO

    # 로거 설정 및 반환
    @staticmethod
    def setup(name):
        """
        고정된 형식에 따른 logger를 return하는 method입니다.

        :param name: logger의 이름을 설정할 수 있습니다. 이 이름으로 봇의 어떤 부분이 로깅됐는지 확인할 수 있습니다.
        :return: 파일 이름, 형식, 이름이 설정된 Logger 객체
        """
        logger = logging.getLogger(name)
        logger.setLevel(Logger.level)
        logger.addHandler(Logger.handler)

        return logger
