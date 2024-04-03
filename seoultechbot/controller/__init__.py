import logging

# DB와 상호작용을 ORM 세션
from sqlalchemy.orm import sessionmaker

# 모델 불러오기
from seoultechbot.model import engine

session = sessionmaker(bind=engine)
logger = logging.getLogger(__name__)
