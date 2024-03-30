# 모듈 불러올 때 초기화 되는 변수들

# 환경 변수 사용을 위해 필요
import os

# 시간 스케쥴러 이용을 위함
import datetime
import sys
from itertools import cycle

# 봇 버전
VERSION = 'v1.3'

# 환경변수를 이용하여 봇 설정 가져오기
DISCORD_BOT_TOKEN = os.getenv("STBOT_DISCORD_BOT_TOKEN")
WEATHER_API_TOKEN = os.getenv("STBOT_WEATHER_API_TOKEN")
PROGRAM_LEVEL = os.getenv("STBOT_PROGRAM_LEVEL", "RELEASE")  # 프로그램 모드
CRAWLING_PERIOD = os.getenv("STBOT_CRAWLING_PERIOD", 60)     # 크롤링 주기(초 단위)
DB_TYPE = os.getenv("STBOT_DB_TYPE", "SQLITE")               # DBMS 설정(SQLITE, MYSQL)

# 로그 생성하기
from seoultechbot.logger import Logger
Logger.set_level(PROGRAM_LEVEL)
logger = Logger.setup('name')

# 봇 토큰이 없을 경우
if not DISCORD_BOT_TOKEN:
    logger.critical('디스코드 봇 토큰을 입력하지 않았습니다. 봇을 종료합니다.')
    sys.exit("디스코드 봇 토큰을 입력하지 않았습니다. 토큰을 입력한 후 다시 시도해주세요.")
else:
    logger.info('디스코드 봇 토큰(앞 10자리): ' + DISCORD_BOT_TOKEN[0:10])

# 날씨 토큰이 없을 경우
if not WEATHER_API_TOKEN:
    logger.warn('오픈 API 기상청 단기예보 조회서비스 토큰을 입력하지 않았습니다. 봇의 날씨 기능이 비활성화 됩니다.')
else:
    logger.info('오픈 API 기상청 단기예보 조회서비스 토큰(앞 10자리): ' + WEATHER_API_TOKEN[0:10])


# 봇 상태 메세지 상태 변수
status = cycle(['도움말: /도움', f'{VERSION}', '봇 시작 중...'])

# 크롤링 스케쥴러 설정
food_notification_time = [datetime.time(hour=i, minute=0,
                                        tzinfo=datetime.timezone(datetime.timedelta(hours=9))) for i in range(9, 13)]
notice_crawling_time = [datetime.time(hour=0, minute=i,
                                      tzinfo=datetime.timezone(datetime.timedelta(hours=9))) for i in range(0, 24, CRAWLING_PERIOD)]
food_crawling_time = [datetime.time(hour=0, minute=i,
                                    tzinfo=datetime.timezone(datetime.timedelta(hours=9))) for i in range(0, 24, CRAWLING_PERIOD)]
