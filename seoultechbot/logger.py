import logging

def setup(name, level=logging.INFO, log_file='seoultechbot_discord.log'):
    logger = logging.getLogger(name)

    # 봇이 디버그 모드일 경우 로깅 레벨을 디버그 모드로 설정
    if level == "DEBUG":
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

    handler = logging.FileHandler(log_file, encoding='utf-8')
    formatter = logging.Formatter('[%(asctime)s][%(name)s] - [%(levelname)s] %(message)s')

    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger
