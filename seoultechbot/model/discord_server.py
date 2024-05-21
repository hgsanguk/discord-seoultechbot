from sqlalchemy import Column, Integer, Boolean
from seoultechbot.model import Base


class DiscordServer(Base):
    """
    봇을 초대한 Discord 서버의 채널 설정 클래스입니다.

    Attributes:
        id: Discord 서버의 id입니다. 데이터베이스에 id로 저장되는 Primary Key입니다.
        cafeteria_menu_notify_time: 해당 서버가 식단 알림을 받을 시간대 입니다. -1일 경우 알림을 받지 않습니다.
        receive_dormitory_notice: 해당 서버가 기숙사 알림을 받는지 체크하는 변수입니다.
        channel_id_notice: Discord 서버 내에서 대학공지사항과 학사일정 알림을 받을 채팅 채널의 id입니다.
        channel_id_cafeteria_menu: Discord 서버 내에서 학식 알림을 받을 채팅 채널의 id입니다.
        # channel_id_notice_colleage_단과대학약칭: Discord 서버 내에서 각 단과대학 알림을 받을 채팅 채널의 id입니다.
        # channel_id_notice_department_학과약칭: Discord 서버 내에서 각 학과 알림을 받을 채팅 채널의 id입니다.
    """
    __tablename__ = 'discord_server'


    # 기본 정보
    id = Column(Integer, primary_key=True)
    cafeteria_menu_notify_time = Column(Integer, nullable=False, default=-1)
    receive_dormitory_notice = Column(Boolean, nullable=False, default=False)

    # 식당 메뉴
    channel_id_cafeteria_menu = Column(Integer, unique=True)  # 제2학생회관, 테크노파크
    # channel_id_cafeteria_menu_kb = Column(Integer, unique=True)  # KB학사
    # channel_id_cafeteria_menu_sung = Column(Integer, unique=True)  # 성림학사
    # channel_id_cafeteria_menu_surim = Column(Integer, unique=True)  # 수림학사

    # 대학공지사항
    channel_id_notice = Column(Integer, unique=True)  # 대학공지사항, 학사일정
    # channel_id_notice_graduate = Column(Integer, unique=True) # 대학원
    # channel_id_notice_job_contest = Column(Integer, unique=True) # 취업, 공모/외부행사

    # 단과대학 공지사항
    # channel_id_notice_college_ice = Column(Integer, unique=True)  # 정보통신대학
    # channel_id_notice_college_engineering = Column(Integer, unique=True)  # 공과대학
    # channel_id_notice_college_nature = Column(Integer, unique=True)  # 에너지바이오대학
    # channel_id_notice_college_human = Column(Integer, unique=True)  # 인문사회대학
    # channel_id_notice_college_and = Column(Integer, unique=True)  # 조형대학
    # channel_id_notice_college_bat = Column(Integer, unique=True)  # 기술경영대학
    # channel_id_notice_college_cccs = Column(Integer, unique=True)  # 창의융합대학
    # channel_id_notice_college_lifelong = Column(Integer, unique=True)  # 미래융합대학

    # 학과 공지사항
    # 정보통신대학
    # channel_id_notice_department_computer = Column(Integer, unique=True)  # 컴퓨터공학과
    # channel_id_notice_department_ee = Column(Integer, unique=True)  # 전자공학과
    # channel_id_notice_department_eie = Column(Integer, unique=True)  # 전기정보공학과
    # channel_id_notice_department_icte = Column(Integer, unique=True)  # 스마트ICT융합공학과
    # 공과대학
    # 에너지바이오대학
    # 인문사회대학
    # 조형대학
    # 기술경영대학
    # 창의융합대학
    # 미래융합대학
