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
    title = Column(String, unique=True, nullable=False)
    image_url = Column(String, name="img_url", nullable=False)


class SecondStudentsUnionBuilding(Base):
    """
    제2학생회관 학생식당의 일일 메뉴 클래스입니다.
    해당 코드 작성 기준 첫번째 메뉴, 두번째 메뉴까지만 판매하므로 최대 두 개의 메뉴까지 지원합니다.

    Attributes:
        id: 데이터베이스에 id로 저장되는 Primary Key입니다. 별도의 용도는 없습니다. (int)
        date: 해당 식단의 날짜입니다. 형식은 YYMMDD입니다. 해당 Attribute는 중복 저장을 막기위해 unique합니다. (int)
        menuN_name: n번째 식단의 주 메뉴 이름입니다. (str)
        menuN_side: n번째 식단의 반찬 이름들입니다. (str)
        menuN_price: n번째 식단의 가격입니다. (str)
    """
    __tablename__ = 'cafeteria_menu_su'

    id = Column(Integer, primary_key=True)
    date = Column(Integer, unique=True)
    menu1_name = Column(String, name="first_name")
    menu1_side = Column(String, name="first_side")
    menu1_price = Column(String, name="first_price")
    menu2_name = Column(String, name="second_name")
    menu2_side = Column(String, name="second_side")
    menu2_price = Column(String, name="second_price")