"""
대표 홈페이지와 기숙사 홈페이지의 공지사항을 스크래핑하는 비동기 메서드를 포함한 파일입니다.
"""
# 비동기 스크래핑과 웹 페이지 파싱을 위한 패키지
import asyncio
from aiohttp import ClientError, ClientSession, ClientTimeout
from aiohttp.http_exceptions import HttpProcessingError
from bs4 import BeautifulSoup

# 링크 Parameter 파싱을 위한 패키지
from urllib.parse import parse_qs, urlparse

# scrapper 패키지의 로거 사용
from seoultechbot.scrapper import logger


async def fetch_all():
    """
    학교 홈페이지의 여러 게시판에서 공지사항을 비동기적으로 가져옵니다.

    :return: `list[list[int, int, str, str], ...]` - 대학공지사항, 학사공지, 장학공지, 기숙사공지의 첫 페이지의 [게시물 번호, 게시판 번호, 게시물 제목, 작성자]
    """

    async def fetch_university(session: ClientSession, board_name: str) -> list:
        """
        `'https://www.seoultech.ac.kr/service/info/' + board_name`\n
        위의 링크(대학교 대표 홈페이지 공지사항)의 첫 페이지를 비동기로 스크래핑 해 게시물 정보를 포함한 코루틴 객체를 반환합니다.
        올바르지 않은 주소를 입력할 경우 `ValueError` 를 발생시킵니다.

        :param session: HTTP GET할 aiohttp의 ClientSession 객체입니다.
        :param board_name: 게시판 이름으로, 대학교 대표 홈페이지 공지사항 링크의 제일 뒤에 들어갈 경로입니다.
        :return: `Coroutine[Any, Any, list]` - list는 [게시물 번호, 게시판 번호, 게시물 제목, 작성자]
        """

        board_list = ['notice', 'matters', 'janghak', 'graduate', 'job']
        if not board_name in board_list:
            raise ValueError('잘못된 게시판 주소를 입력하였습니다.')

        link = f'https://www.seoultech.ac.kr/service/info/{board_name}'
        try:
            async with session.get(link) as response:
                if response.status != 200:
                    raise HttpProcessingError(code=response.status, message='HTTP 오류 발생')

                text = await response.text()
                parser = BeautifulSoup(text, "html.parser")
                rows = parser.select('.tbl_list > tbody:nth-child(4) > tr')
                notice = []
                for row in rows:
                    try:
                        # 게시물 제목 찾기
                        title = row.find(class_='tit dn2') or row.find('div')
                        if not title:
                            logger.warning(f"대표 홈페이지의 {board_name} 게시판에서 예상한 구조와 다른 구조의 게시물을 감지: 제목 element select 실패")
                            continue

                        title_text = title.getText(strip=True)
                        author_class = 'dn4' if row.find(class_='tit dn2') else 'dn5'
                        author = row.find(class_=author_class).getText(strip=True)

                        # 게시물 번호 파싱
                        url = row.find('a')['href']
                        notice_num = int(parse_qs(urlparse(url).query).get('bnum', None)[0])
                        board_num = int(parse_qs(urlparse(url).query).get('bidx', None)[0])
                        notice.append([notice_num, board_num, title_text, author])
                        logger.debug(f"대표 홈페이지의 {board_name} 게시판에서 {board_num}번 게시물 스크래핑")
                    except AttributeError as e:
                        logger.warning(f"대표 홈페이지의 {board_name} 게시판에서 예상한 구조와 다른 구조의 게시물을 감지: {e}")
                        continue
                logger.info(f"대표 홈페이지의 {board_name} 게시판 스크래핑 완료")
                return notice
        except ClientError as e:
            logger.error(f"대표 홈페이지의 {board_name} 게시판 HTTP 요청 실패: {e}")
        except HttpProcessingError as e:
            logger.error(f"대표 홈페이지의 {board_name} 게시판에서 HTTP 에러 발생: {e}")
        except Exception as e:
            logger.error(f"대표 홈페이지의 {board_name} 게시판에서 알 수 없는 오류 발생: {e}")
        return []

    # 대학공지사항, 학사공지, 장학공지, 기숙사공지 스크래핑
    timeout = ClientTimeout(total=10)  # 10초 타임아웃 설정
    async with ClientSession(timeout=timeout) as session:
        tasks = [fetch_university(session, 'notice'), fetch_university(session, 'matters'),
                 fetch_university(session, 'janghak')]
        results = await asyncio.gather(*tasks, return_exceptions=True)  # 예외가 발생해도 크래시 되지 않도록 설정
        return results
