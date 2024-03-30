from sqlalchemy import Column, Integer, String
from seoultechbot.model import Base


class Notice:
    """
    Attributes:
        board_no (int): 게시글의 번호입니다. 데이터베이스에 id로 저장되는 Primary Key입니다.
        category (str): 게시글이 올라온 카테고리입니다.

        # title (str): 게시글의 제목입니다.
        # author (str): 게시글의 게시자입니다.
        # scrapped_time (str): 스크래핑 된 시간을 통해 추정한 게시글이 올라온 시각입니다.
        # content (str): 게시글의 내용입니다.
    """
    board_no = Column(Integer, name='id', primary_key=True)
    category = Column(String, nullable=False)

    # title = Column(String, nullable=False)
    # author = Column(String, nullable=False)
    # scrapped_time = Column(String, nullable=False)
    # content = Column(String)


class University(Notice, Base):
    """
    대학교 홈페이지에서 스크래핑한 공지사항의 클래스입니다.
    카테고리로 현재 `대학공지사항, 학사공지, 장학공지, 생활관공지` 가 있습니다.
    """
    __tablename__ = 'notice_university'


# class Colleage(Notice, Base):
#     """
#     단과대학 홈페이지에서 스크래핑한 공지사항의 클래스입니다.
#     """
#     __tablename__ = 'notice_colleage'
#
#
# class Department(Notice, Base):
#     """
#     학과 홈페이지에서 스크래핑한 공지사항의 클래스입니다.
#     """
#     __tablename__ = 'notice_department'
