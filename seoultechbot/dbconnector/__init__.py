# 추상 클래스
from abc import ABC, abstractmethod

# 로거 가져오기
import seoultechbot
from seoultechbot.dbconnector.mysql import MySQLConnector
from seoultechbot.dbconnector.sqlite import SQLiteConnector

logger = seoultechbot.Logger.setup('db-connector')

# DB Connector 선택
if seoultechbot.DB_MODE == "MYSQL" or "MARIADB":
    dbconnector = MySQLConnector()
else:
    dbconnector = SQLiteConnector()

class DBConnector(ABC):
    @abstractmethod
    def open_connection(self):
        """데이터베이스 연결 열기"""
        pass

    @abstractmethod
    def close_connection(self):
        """데이터베이스 연결 닫기"""
        pass

    @abstractmethod
    def execute_query(self, query):
        """SQL 쿼리 실행 및 결과 반환"""
        pass
