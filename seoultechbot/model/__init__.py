"""
sqlalchemy ORM을 사용하여 봇의 데이터베이스 모델을 관리하는 패키지입니다.
"""
# 환경변수 가져오기 위한 라이브러리
import os

# 오류 시 종료를 위한 라이브러리
import sys

# 로거 설정을 위한 라이브러리
import logging

# DB와 상호작용을 위한 ORM
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.exc import SQLAlchemyError

# 데이터베이스 초기화를 위한 import
from .base import Base
from .cafeteria_menu import SeoulTechnoparkCafeteriaMenu, SecondStudentsUnionBuildingCafeteriaMenu
from .notice import UniversityNotice
from .server_config import ServerConfig
from seoultechbot.config import Config

# 로거 가져오기
logger = logging.getLogger(__name__)


async def init_db():
    # DB에 연결 및 초기화
    try:
        engine = create_async_engine(Config().db_connection_str)
        logger.info(f"데이터베이스에 연결 완료")
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info(f"데이터베이스 초기화 완료")
    except SQLAlchemyError as e:
        logger.exception(f"데이터베이스에 초기화 도중 오류 발생: {e}")
        sys.exit("데이터베이스 초기화 중 오류가 발생하여 봇을 종료합니다. DB 서버의 상태와 입력한 정보가 올바른지 확인한 후 다시 시도해주세요.")
