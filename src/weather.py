import requests
from datetime import datetime, timedelta


def get_weather(token, added_time):
    today = datetime.now()
    req_time = today + timedelta(hours=added_time)
    url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtFcst'
    direction = ['북', '북북동', '북동', '동북동', '동', '동남동', '남동', '남남동', '남', '남남서', '남서',
                 '서남서', '서', '서북서', '북서', '북북서', '북']

    basetime = today
    if int(basetime.strftime('%H%M')[2:4]) < 45:
        basetime = today - timedelta(hours=1)
    else:
        req_time = req_time + timedelta(hours=1)

    params = {'serviceKey': token, 'dataType': 'JSON', 'numOfRows': '1000', 'base_date': basetime.strftime('%Y%m%d'),
              'base_time': basetime.strftime('%H') + '30', 'nx': '61', 'ny': '128'}

    response = requests.get(url, params=params)
    items = response.json().get('response').get('body').get('items')

    data = ['0', '0', []]
    weather_data = ['오류', '오류', '오류', '오류', '오류', '오류', '오류', '오류', '오류']

    data[0] = today + timedelta(hours=added_time)
    for item in items['item']:
        if item['fcstTime'] == req_time.strftime('%H') + '00':
            data[1] = item['fcstTime']

            # 기온
            if item['category'] == 'T1H':
                weather_data[0] = item['fcstValue']

            # 하늘 상태
            if item['category'] == 'SKY':
                weather_data[1] = item['fcstValue']

                if weather_data[1] == '1':
                    weather_data[2] = ':sunny: 맑음'
                elif weather_data[1] == '3':
                    weather_data[2] = ':white_sun_cloud: 구름많음'
                elif weather_data[1] == '4':
                    weather_data[2] = ':cloud: 흐림'
                else:
                    weather_data[2] = 'API 에러'

            # 강수 형태
            if item['category'] == 'PTY':
                weather_data[3] = item['fcstValue']

            # 강수량
            if item['category'] == 'RN1':
                weather_data[4] = item['fcstValue']

            # 습도
            if item['category'] == 'REH':
                weather_data[5] = item['fcstValue']

            # 풍향
            if item['category'] == 'VEC':
                weather_data[6] = item['fcstValue']
                direction_num = int((int(item['fcstValue']) + 22.5 * 0.5) / 22.5)
                weather_data[7] = direction[direction_num]

            # 풍속
            if item['category'] == 'WSD':
                weather_data[8] = item['fcstValue']

    data[2] = weather_data
    return data

