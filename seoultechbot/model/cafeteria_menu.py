from sqlalchemy import Column, Integer, String
from seoultechbot.model import Base


class SeoulTechnopark(Base):
    """
    서울테크노파크 구내식당의 일일 메뉴 클래스입니다.

    Attributes:
        id (int): 서울테크노파크 홈페이지에 올라오는 식단의 게시물 고유번호입니다. 데이터베이스에 id로 저장되는 Primary Key입니다.
        week (int): 식단의 연도와 주차로, 형식은 `YYWW` 입니다. 해당 Attribute는 중복 저장을 막기 위해 unique합니다.
        title (str): 서울테크노파크 홈페이지에 올라오는 식단의 게시물 제목입니다. 해당 달의 몇 번째 주 식단표인지 표시하기 위해 사용합니다.
        image_link (str): 서울테크노파크의 식단의 게시물 내의 식단 이미지 링크입니다.
    """

    __tablename__ = 'cafeteria_menu_stp'

    id = Column(Integer, primary_key=True)
    week = Column(Integer, unique=True)
    title = Column(String, nullable=False)
    image_url = Column(String, name="img_url", nullable=False)


class SecondStudentsUnionBuilding(Base):
    """
    제2학생회관 학생식당의 일일 메뉴 클래스입니다.
    해당 코드 작성 기준 첫번째 메뉴, 두번째 메뉴까지만 판매하므로 최대 두 개의 메뉴까지 지원합니다.

    Attributes:
        date: 해당 식단의 날짜로, 형식은 YYMMDD입니다. 데이터베이스에 id로 저장되는 Primary Key입니다. (int)
        lunch_a_name: 점심 A 코너의 이름입니다. (str)
        lunch_a_price: 점심 A 코너의 가격입니다. (str)
        lunch_a_menu: 점심 A 코너의 메뉴입니다. (str)
        lunch_b_name: 점심 B 코너의 이름입니다. (str)
        lunch_b_price: 점심 B 코너의 가격입니다. (str)
        lunch_b_menu: 점심 B 코너의 메뉴입니다. (str)
        dinner_name: 저녁 코너의 이름입니다. (str)
        dinner_price: 저녁 코너의 가격입니다. (str)
        dinner_menu: 저녁 코너의 메뉴입니다. (str)
    """
    __tablename__ = 'cafeteria_menu_su'

    date = Column(Integer, primary_key=True)
    lunch_a_name = Column(String, name="lunch_a_name")
    lunch_a_price = Column(String, name="lunch_a_price")
    lunch_a_menu = Column(String, name="lunch_a_menu")
    lunch_b_name = Column(String, name="lunch_b_name")
    lunch_b_price = Column(String, name="lunch_b_price")
    lunch_b_menu = Column(String, name="lunch_b_menu")
    dinner_name = Column(String, name="dinner_name")
    dinner_price = Column(String, name="dinner_price")
    dinner_menu = Column(String, name="dinner_menu")
