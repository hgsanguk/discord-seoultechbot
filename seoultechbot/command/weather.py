# Discord 명령 전송을 위한 라이브러리
from datetime import datetime

# 로거 설정을 위한 라이브러리
import logging

# Discord 명령 전송을 위한 패키지
import discord
from discord import app_commands
from discord.ext import commands

# 날씨 정보 가져오는 모듈
from seoultechbot import scrapper


class Weather(commands.Cog):
    """
    봇의 `/날씨` 명령어 사용에 필요한 메서드를 모아놓은 클래스입니다.
    """
    def __init__(self, bot):
        self.__logger = logging.getLogger(__name__)
        self.__bot = bot
        self.__logger.debug(f'{__name__} 모듈 초기화 완료')

    @app_commands.command(name='날씨', description='현재 캠퍼스의 날씨와 1 ~ 6시간 뒤 날씨 예보를 보여줍니다.')
    async def weather(self, interaction: discord.Interaction):
        # 로그 기록
        self.__logger.info(f"{interaction.guild.name}({interaction.guild.id})의 {interaction.channel.name}({interaction.channel.id})에서 '/날씨' 사용")

        # 명령어를 사용한 시각
        date = datetime.now()

        # 시간대별 Embed 색상 설정
        if 8 <= date.hour <= 16:
            color = 0x99CCFF
        elif 5 <= date.hour < 8:
            color = 0xFAEBD7
        elif 16 < date.hour < 19:
            color = 0xF29886
        else:
            color = 0x000080

        # 하늘 상태 dict
        sky_dict = {'1': {'name': '맑음', 'emoji': ':sunny:'},
                    '3': {'name': '구름많음', 'emoji': ':white_sun_cloud:'},
                    '4': {'name': '흐림', 'emoji': ':cloud:'}}
        # 강수 형태 dict
        pty_dict = {'1': {'name': '비', 'emoji': ':umbrella:'},
                    '2': {'name': '눈비', 'emoji': ':umbrella:/:snowman2:'},
                    '3': {'name': '눈', 'emoji': ':snowman2:'},
                    '4': {'name': '소나기', 'emoji': ':white_sun_rain_cloud:'},  # 초단기예보에는 소나기 코드가 없으나 일단 넣음
                    '5': {'name': '빗방울', 'emoji': ':sweat_drops:'},
                    '6': {'name': '진눈깨비', 'emoji': ':sweat_drops:/:snowflake:'},
                    '7': {'name': '싸락눈', 'emoji': ':snowflake:'}}

        # 정보를 가져올 때까지 대기
        await interaction.response.defer()

        # 날씨 정보 가져오기
        result = await scrapper.weather.fetch(date)
        if not result:
            await interaction.followup.send('날씨를 불러오는 중 문제가 발생했습니다. 다시 시도해주세요.')
        else:
            result = list(result.items())  # 반복을 위해 list로 변환 (result[i][0]: 시간(HHMM), result[i][1]: 예보값)

            # 제목
            embed = discord.Embed(title="이 시간 캠퍼스 날씨",
                                  description=f'{date.month}월 {date.day}일 {date.hour}시 {date.minute}분 공릉동의 날씨입니다.',
                                  color=color)

            # 현재 날씨 초단기예보 처리
            temperature_str = ':thermometer: 기온: ' + result[0][1]['T1H'] + '°C'
            humidity_str = ':droplet: 습도: ' + result[0][1]['REH'] + '%'
            wind_str = (':dash: 바람: ' + Weather.__convert_degree_to_direction(result[0][1]['VEC']) +
                        '(' + result[0][1]['VEC'] + '°) 방향으로 ' + result[0][1]['WSD'] + 'm/s')
            if result[0][1]['PTY'] == '0':
                sky_name = sky_dict[result[0][1]['SKY']]['name']
                sky_emoji = sky_dict[result[0][1]['SKY']]['emoji']
            else:
                sky_name = pty_dict[result[0][1]['PTY']]['name']
                sky_emoji = pty_dict[result[0][1]['PTY']]['emoji']
            embed.add_field(name=f"{sky_emoji} {sky_name}\n{temperature_str}", value=f"{humidity_str}\n{wind_str}", inline=False)

            # 1 ~ 6시간 뒤 날씨 초단기예보 처리
            forcast_str = ''
            for i in range(1, 6):
                time_str = f'**{result[i][0][1] if int(result[i][0][0:2]) < 10 else result[i][0][0:2]}시**'
                temperature_str = result[i][1]['T1H'] + '°C'
                humidity_str = ':droplet: ' + result[i][1]['REH'] + '%'
                if result[i][1]['PTY'] == '0':
                    sky_emoji = sky_dict[result[i][1]['SKY']]['emoji']
                else:
                    sky_emoji = pty_dict[result[i][1]['PTY']]['emoji']
                forcast_str += f"{time_str}: {sky_emoji} {temperature_str}, {humidity_str}\n"
            embed.add_field(name='날씨 예보', value=forcast_str, inline=False)

            # 주의 사항
            embed.set_footer(text='기상청 초단기예보 조회 서비스 오픈 API를 이용한 것으로, 실제 기상상황과 차이가 있을 수 있습니다.')

            # 결과 전송
            self.__logger.info(f"{interaction.guild.name}({interaction.guild.id})의 {interaction.channel.name}({interaction.channel.id})에서 '/날씨' 응답 전송 성공")
            await interaction.followup.send(embed=embed)

    @staticmethod
    def __convert_degree_to_direction(degree: str) -> str:
        # 풍향값 리스트, 별도의 식으로 계산한 index를 통해 풍향을 결정
        directions = ['북', '북북동', '북동', '동북동', '동', '동남동', '남동', '남남동',
                      '남', '남남서', '남서', '서남서', '서', '서북서', '북서', '북북서', '북']

        return directions[int((int(degree) + 22.5 * 0.5) / 22.5)]


async def setup(bot):
    await bot.add_cog(Weather(bot))
