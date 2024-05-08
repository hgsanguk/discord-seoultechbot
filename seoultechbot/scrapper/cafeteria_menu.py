"""
학교 홈페이지와 서울테크노파크 홈페이지의 식당 메뉴 스크래핑에 관한 파일입니다.
"""
# 날짜 계산을 위한 패키지
from datetime import datetime, timedelta

# 비동기 스크래핑과 웹 페이지 파싱을 위한 패키지
import asyncio
from aiohttp import ClientError, ClientSession, ClientTimeout
from aiohttp.http_exceptions import HttpProcessingError
from bs4 import BeautifulSoup

# 로거 가져오기
import logging
logger = logging.getLogger(__name__)


async def fetch_su_building(start_date: datetime) -> dict:
    """
    학교 홈페이지에서 제2학생회관의 식단을 시작일부터 그 주의 금요일까지 비동기적으로 가져옵니다.

    :param start_date: 시작일 (datetime)
    :return: `dict` - Key: 날짜 (int) / Value: 식단{코너 이름, 가격, 메뉴} (dict)
    """
    def extract_menu_info(row):
        return {
            'name': row.select_one('td:nth-child(1)').getText(strip=True),
            'price': row.select_one('td:nth-child(2)').getText(strip=True),
            'menu': row.select_one('td:nth-child(3)').getText('\n', strip=True)
        }

    async def fetch_menu_for_date(session: ClientSession, target_date: datetime) -> dict:
        """
        학교 홈페이지에서 제2학생회관의 식단을 시작일부터 그 주의 금요일까지 비동기적으로 가져옵니다.

        :param session: HTTP GET할 aiohttp의 ClientSession 객체
        :param target_date: 스크래핑을 시작할 날짜 (datetime)
        :return: `dict` - 점심/저녁의 코너 이름, 가격, 메뉴
        """
        date_str = target_date.strftime("%Y-%m-%d")
        link = 'https://www.seoultech.ac.kr/life/student/food2/?location_code=20&food_date=' + date_str
        try:
            async with session.get(link) as response:
                if response.status != 200:
                    raise HttpProcessingError(code=response.status, message='HTTP 오류 발생')

                html = await response.text()
                parser = BeautifulSoup(html, 'html.parser')
                menu_div = parser.select_one('.dts_design > div:nth-child(5)')
                lunch_rows = menu_div.select('div:nth-child(2) > table:nth-child(1) > tr')
                dinner_rows = menu_div.select_one('div:nth-child(4) > table:nth-child(1) > tr:nth-child(3)')

                # 식단표가 없을 경우
                if menu_div.getText(strip=True) == "등록된 식단표가 없습니다.":
                    logger.info(f"제2학생회관의 {target_date.year}년 {target_date.month}월 {target_date.day}일 식단 업로드 되지 않음")
                    return {}

                # 메뉴 정보 추출
                menu = {'lunch_a': extract_menu_info(lunch_rows[1]),
                        'lunch_b': extract_menu_info(lunch_rows[2]),
                        'dinner': extract_menu_info(dinner_rows)}

                logger.info(f"제2학생회관의 {target_date.year}년 {target_date.month}월 {target_date.day}일 식단 스크래핑 완료")
                return menu

        except ClientError as e:
            logger.exception(f"제2학생회관의 {target_date.year}년 {target_date.month}월 {target_date.day}일 식단 HTTP 요청 실패: {e}")
        except HttpProcessingError as e:
            logger.exception(f"제2학생회관의 {target_date.year}년 {target_date.month}월 {target_date.day}일 식단 페이지 요청 중 HTTP 에러 발생: {e}")
        except Exception as e:
            logger.exception(f"제2학생회관의 {target_date.year}년 {target_date.month}월 {target_date.day}일 식단 페이지 요청 중 알 수 없는 오류 발생: {e}")
        return {}

    # 시작일부터 그 주의 금요일까지 식단을 비동기적으로 스크래핑
    async with ClientSession(timeout=ClientTimeout(total=10)) as session:
        tasks = {int((start_date + timedelta(days=i)).strftime("%Y%m%d")):
                     fetch_menu_for_date(session, start_date + timedelta(days=i)) for i in range(5 - start_date.weekday())}
        results = await asyncio.gather(*tasks.values(), return_exceptions=True)  # 예외가 발생해도 크래시 되지 않도록 설정
        # 날짜와 스크래핑 결과 쌍을 dict로 변환
        return dict(zip(tasks.keys(), results))


async def fetch_technopark() -> dict:
    """
    서울테크노파크 홈페이지의 식단표 게시판에서 최신 게시물의 식단표 정보를 비동기적으로 가져옵니다.

    :return: `dict` - {'id': 게시물 번호, 'title': 게시물 제목, 'img_url': 식단표 이미지 링크}
    """
    async def fetch(url: str, session: ClientSession):
        async with session.get(url) as response:
            if response.status != 200:
                raise HttpProcessingError(code=response.status, message='HTTP 오류 발생')
            return await response.text()

    board_link = 'https://www.seoultp.or.kr/user/nd70791.do'  # 식단표 게시판 링크
    try:
        async with ClientSession(timeout=ClientTimeout(total=10)) as session:
            html = await fetch(board_link, session)
            parser = BeautifulSoup(html, "html.parser")

            # 최신 식단표 게시물 선택
            newest_post = parser.select_one('.board-list > tbody:nth-child(4) > tr:nth-child(1)')
            title = newest_post.select_one('td:nth-child(2) > a:nth-child(1)')
            post_num = title['href'].split("'")[5]
            title_text = title.getText(strip=True)

            # 최신 식단표 게시물 페이지 요청 및 이미지 링크 선택
            post_link = board_link + '?View&boardNo=' + post_num
            html = await fetch(post_link, session)
            parser = BeautifulSoup(html, "html.parser")
            content = parser.select_one('.board-write > tbody:nth-child(3) > tr:nth-child(4)')
            img_url = 'https://www.seoultp.or.kr' + content.find(name='img')['src']

            logger.info(f"서울테크노파크의 {title_text} 스크래핑 완료")
            result = {'id': int(post_num), 'title': title_text, 'img_url': img_url}
            return result

    except ClientError as e:
        logger.exception(f"서울테크노파크 홈페이지 HTTP 요청 실패: {e}")
    except HttpProcessingError as e:
        logger.exception(f"서울테크노파크 홈페이지 요청 중 HTTP 에러 발생: {e}")
    except Exception as e:
        logger.exception(f"서울테크노파크 홈페이지에서 알 수 없는 오류 발생: {e}")
    return {}
