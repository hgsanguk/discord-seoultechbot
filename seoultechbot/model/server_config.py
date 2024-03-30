from sqlalchemy import Column, Integer, Boolean
from seoultechbot.model import Base


class ServerConfig(Base):
    """
    봇을 초대한 Discord 서버의 봇 설정 클래스입니다.

    Attributes:
        server_id (int): Discord 서버의 ID입니다. 데이터베이스에 id로 저장되는 Primary Key입니다.
        channel_id (int): Discord 서버 내에서 알림을 받을 Channel ID입니다.
        cafeteria_menu_notify_time (int): 해당 서버가 식단 알림을 받을 시간대 입니다. -1일 경우 알림을 받지 않습니다.
        receive_dormitory_notice (str): 해당 서버가 기숙사 알림을 받는지 체크하는 변수입니다.
    """
    __tablename__ = 'server_config'

    server_id = Column(Integer, name='id', primary_key=True)
    channel_id = Column(Integer, name='channel', unique=True, nullable=False)
    cafeteria_menu_notify_time = Column(Integer, nullable=False)
    receive_dormitory_notice = Column(Boolean, nullable=False)