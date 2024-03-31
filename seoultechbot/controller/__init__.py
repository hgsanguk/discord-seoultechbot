# DB와 상호작용을 ORM 세션
from sqlalchemy.orm import sessionmaker

import seoultechbot
# 모델 불러오기
from seoultechbot.model import engine
import seoultechbot.scrapper

session = sessionmaker(bind=engine)
logger = seoultechbot.Logger.setup('seoultechbot.controller')
