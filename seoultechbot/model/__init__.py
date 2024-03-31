"""
sqlalchemy ORM을 사용하여 봇의 데이터베이스 모델을 관리하는 패키지입니다.
"""
import os
import sys

# DB와 상호작용을 위한 ORM
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.exc import SQLAlchemyError

import seoultechbot

# 로거 가져오기
logger = seoultechbot.Logger.setup('seoultechbot.model')

HOST = os.getenv("STBOT_DB_HOST")
PORT = os.getenv("STBOT_DB_PORT", 3306)
NAME = os.getenv("STBOT_DB_NAME")
USER = os.getenv("STBOT_DB_USER")
PASSWORD = os.getenv("STBOT_DB_PASSWORD")

# 어떤 DB를 사용하는지 체크하고 연결 시도
if seoultechbot.DB_TYPE == "MYSQL" or "MARIADB":
    # MySQL 혹은 MariaDB
    try:
        conn_str = f"mysql+mysqldb://{USER}:{PASSWORD}@{HOST}:{PORT}/{NAME}"
        engine = create_engine(conn_str)
        logger.debug(f"{conn_str}에 연결 중...")
        engine.connect()
        logger.info(f"{seoultechbot.DB_TYPE}에 연결 완료")
    except SQLAlchemyError as e:
        engine = None
        logger.error(f"{seoultechbot.DB_TYPE}에 연결 도중 오류 발생: {e}")
        sys.exit(f"{seoultechbot.DB_TYPE}에 연결 도중 오류 발생하여 봇을 종료합니다. 입력한 정보가 올바른지 확인한 후 다시 시도해주세요.")
else:
    # SQLite
    engine = create_engine('sqlite://../../seoultechbot-discord.db')

Base = declarative_base()
Base.metadata.create_all(engine)
