# 추상 클래스
from abc import ABC, abstractmethod

# 로거 가져오기
import seoultechbot
logger = seoultechbot.logger.setup('db-connector')


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
