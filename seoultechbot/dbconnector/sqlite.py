# DB Connector
import sqlite3
from seoultechbot import DBConnector
from seoultechbot.dbconnector import logger


class SQLiteConnector(DBConnector):
    config = 'seoultechbot_discord.db'
    conn = None

    def open_connection(self):
        """SQLite 데이터베이스 연결"""
        try:
            self.conn = sqlite3.connect(self.config)
            if self.conn.cursor():
                logger.info("로컬 SQLite DB(" + self.config + ")에 연결 완료")
        except sqlite3.Error as e:
            logger.error("로컬 SQLite DB(" + self.config + ")에 연결 실패: " + str(e))
            logger.error("DB에 연결할 수 없으므로 봇을 종료합니다.")
            exit(-1)

    def close_connection(self):
        """SQLite 데이터베이스 연결 끊기"""
        if self.conn is not None:
            self.conn.close()
            logger.info("로컬 SQLite DB(" + self.config + ")와 연결 종료")

    def execute_query(self, query):
        """SQL 쿼리 실행 및 결과 반환"""
        cursor = self.conn.cursor()
        try:
            cursor.execute(query)
            result = cursor.fetchall()
            return result
        except sqlite3.Error as e:
            print("로컬 SQLite DB(" + self.config + ")에 쿼리 요청 오류: " + str(e))
        finally:
            cursor.close()