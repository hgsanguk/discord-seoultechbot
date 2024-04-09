"""
대학교 학사 일정의 비동기 스크래핑에 관한 모듈입니다.
"""
# 자세한 예외 발생 로그 출력을 위한 패키지
import traceback

# 비동기 스크래핑과 웹 페이지 파싱을 위한 패키지
from datetime import datetime
from aiohttp import ClientError, ClientSession, ClientTimeout
from aiohttp.http_exceptions import HttpProcessingError
from bs4 import BeautifulSoup

# scrapper 패키지의 로거 사용
from seoultechbot.scrapper import logger


async def fetch_academic_calendar(target_date: datetime) -> list:
    """
    `'https://eclass.seoultech.ac.kr/ilos/main/main_schedule_view.acl?viewDt=' + target_date.strftime('%Y%m%d')`\n
    위의 링크(학교 e-Class의 학사 일정)을 비동기로 스크래핑 해 학사 일정을 담은 리스트를 반환합니다.

    :param target_date: 스크래핑을 원하는 학사 일정 날짜의 datetime 입니다.
    :return: `list[str]` - 학사 일정
    """
    async with ClientSession(timeout=ClientTimeout(total=10)) as session:
        date = target_date.strftime('%Y%m%d')  # 오늘 날짜
        try:
            async with session.get(f'https://eclass.seoultech.ac.kr/ilos/main/main_schedule_view.acl?viewDt={date}') as response:
                if response.status != 200:
                    raise HttpProcessingError(code=response.status, message='HTTP 오류 발생')
                html = await response.text()
                parser = BeautifulSoup(html, "html.parser")

                # 학사 일정 가져오기
                rows = parser.find_all(class_='changeDetile schedule-Detail-Box')
                schedule = []

                # 리스트에 학사 일정 추가
                for row in rows:
                    schedule.append(row.text.strip())
                logger.info(f"{date}의 학교 학사 일정 {len(schedule)}개 스크래핑 완료")
                return schedule
        except ClientError as e:
            logger.error(f"기숙사 홈페이지 HTTP 요청 실패: {e}")
        except HttpProcessingError as e:
            logger.error(f"기숙사 홈페이지 요청 중 HTTP 에러 발생: {e}")
        except Exception as e:
            logger.error(f"기숙사 홈페이지에서 알 수 없는 오류 발생: {e}")
            logger.error(traceback.format_exc())
        return []
