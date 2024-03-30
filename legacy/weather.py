import requests
from datetime import datetime, timedelta


def get_weather(token):
    today = datetime.now()
    url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtFcst'
    direction = ['북', '북북동', '북동', '동북동', '동', '동남동', '남동', '남남동', '남', '남남서', '남서',
                 '서남서', '서', '서북서', '북서', '북북서', '북']

    basetime = today
    if int(basetime.strftime('%H%M')[2:4]) < 45:
        basetime = today - timedelta(hours=1)

    params = {'serviceKey': token, 'dataType': 'JSON', 'numOfRows': '1000', 'base_date': basetime.strftime('%Y%m%d'),
              'base_time': basetime.strftime('%H') + '30', 'nx': '61', 'ny': '128'}

    response = requests.get(url, params=params, timeout=20)
    items = response.json().get('response').get('body').get('items')

    data = [[], [], [], [], [], []]

    for i, item in enumerate(items['item']):
        if i < 6:
            data[i] = ['기온', '하늘 상태 번호', '하늘 상태', '강수 형태', '강수량', '습도', '풍각', '풍향', '풍속', '예보 시간']
            if int(item['fcstTime'][0:2]) < 10:
                data[i % 6][9] = item['fcstTime'][1]
            else:
                data[i % 6][9] = item['fcstTime'][0:2]

        # 강수 형태 (PTY)
        elif 6 <= i < 12:
            data[i % 6][3] = item['fcstValue']

        # 강수량 (RN1)
        elif 12 <= i < 18:
            data[i % 6][4] = item['fcstValue']

        # 하늘 상태 (SKY)
        elif 18 <= i < 24:
            if item['fcstValue'] == '1':
                data[i % 6][1] = ':sunny:'
                data[i % 6][2] = '맑음'
            elif item['fcstValue'] == '3':
                data[i % 6][1] = ':white_sun_cloud:'
                data[i % 6][2] = '구름많음'
            elif item['fcstValue'] == '4':
                data[i % 6][1] = ':cloud:'
                data[i % 6][2] = '흐림'
            else:
                data[i % 6][1] = ':warning:'
                data[i % 6][2] = 'API 에러'

        # 기온 (TH1)
        elif 24 <= i < 30:
            data[i % 6][0] = item['fcstValue']

        # 습도 (REH)
        elif 30 <= i < 36:
            data[i % 6][5] = item['fcstValue']

        # 풍향 (VEC)
        elif 48 <= i < 54:
            data[i % 6][6] = item['fcstValue']
            direction_num = int((int(item['fcstValue']) + 22.5 * 0.5) / 22.5)
            data[i % 6][7] = direction[direction_num]

        # 풍속 (WSD)
        elif 54 <= i < 60:
            data[i % 6][8] = item['fcstValue']

    return today, data
