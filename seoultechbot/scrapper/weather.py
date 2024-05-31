# 환경변수에서 토큰을 가져오기 위한 라이브러리
import os

# 시간 계산을 위한 라이브러리
from datetime import datetime, timedelta

# 비동기 요청을 위한 패키지
from aiohttp import ClientError, ClientSession, ClientTimeout
from aiohttp.http_exceptions import HttpProcessingError

# API 응답 예외 처리를 위한 import
from seoultechbot.exception import AbnormalResultCodeFromOpenAPIException

# 로거 가져오기
import logging
logger = logging.getLogger(__name__)


async def fetch(target_time: datetime) -> dict:
    """
    `http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtFcst`\n
    위의 링크에서 초단기예보를 요청하여 시간 순으로 정렬한 초단기예보 정보를 반환합니다.
    자세한 사항은 공공데이터포털의 활용 가이드(https://www.data.go.kr/tcs/dss/selectApiDataDetailView.do?publicDataPk=15084084)를 참고해주세요.

    :param target_time: 예보를 가져오길 원하는 기준 시각의 datetime 입니다.
    :return: `dict` - 시간에 대하여 정렬된 초단기예보 정보 `{HHMM(시간): PTY(강수 형태), RN1(시간 당 강수량), SKY(하늘 상태), T1H(기온), REH(습도), VEC(풍향), WSD(풍속)}, ...`
    """
    url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtFcst'

    # 45분에 해당 시각의 초단기예보가 발표되므로, 45분 이전일 경우 이전 시간의 예보를 사용
    base_time = target_time - timedelta(hours=1) if int(target_time.minute) < 45 else target_time

    # Parameter
    params = {'serviceKey': os.getenv('STBOT_WEATHER_API_TOKEN'), 'dataType': 'JSON', 'numOfRows': '1000',
              'base_date': base_time.strftime('%Y%m%d'), 'base_time': base_time.strftime('%H') + '30',
              'nx': '62', 'ny': '128'}
    session = ClientSession(timeout=ClientTimeout(total=10))
    try:
        async with session.get(url, params=params) as response:
            if response.status != 200:
                raise HttpProcessingError(code=response.status, message='HTTP 오류 발생')

            result = (await response.json())['response']
            header = result['header']

            # API 서버가 00(정상) 외의 응답 코드를 보냈을 경우 예외 처리
            if header['resultCode'] != '00':
                raise AbnormalResultCodeFromOpenAPIException(header['resultCode'], header['resultMsg'])
            logger.info('공공데이터포털로 부터 날씨 데이터 정상 수신')

            # API 결과
            items = result['body']['items']

            # 결과를 저장할 빈 dict
            # PTY: 강수 형태, RN1: 시간 당 강수량(mm), SKY: 하늘 상태
            # T1H: 기온(C), REH: 습도(%), VEC: 풍향(deg), WSD: 풍속(m/s)
            result_dict = {}

            # 제외할 예보값 리스트
            # VVV: 남북바람성분(m/s), UUU: 동서바람성분(m/s), LGT: 낙뢰(kA)
            exclude_categories = ['VVV', 'UUU', 'LGT']

            # 예보 시각(fcstTime의 Key)에 대하여 여러 종류의 예보값(fcstValue의 Key, Value)을 정렬
            for item in items['item']:
                fcst_time = item['fcstTime']
                category = item['category']

                if category not in exclude_categories:
                    if fcst_time not in result_dict:
                        result_dict[fcst_time] = {}
                    result_dict[fcst_time][category] = item['fcstValue']

            logger.debug(f'날씨 데이터 처리 완료: {result_dict}')
            await session.close()
            return result_dict
    except ClientError as e:
        logger.exception(f"공공데이터포털에 HTTP 요청 실패: {e}")
    except HttpProcessingError as e:
        logger.exception(f"공공데이터포털에 학교 학사 일정 요청 중 HTTP 에러 발생: {e}")
    except AbnormalResultCodeFromOpenAPIException as e:
        logger.exception(f"공공데이터포털에서 적절하지 않은 응답 코드를 받음: {e}")
    except TimeoutError as e:
        logger.exception(f"공공데이터포털의 응답시간 초과: {e}")
    except Exception as e:
        logger.exception(f"공공데이터포털에서 알 수 없는 오류 발생: {e}")
    await session.close()
    return {}
