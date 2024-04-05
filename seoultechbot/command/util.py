import logging

import discord
from discord import app_commands
from discord.ext import commands


class Util(commands.Cog):
    """
    봇의 작동과 사용에 유용한 명령어를 모아놓은 클래스입니다.
    """
    def __init__(self, bot):
        self.__logger = logging.getLogger(__name__)
        self.__bot = bot
        self.__logger.debug(f'{__name__} 모듈 초기화 완료')

    @app_commands.command(name='핑', description='봇과 Discord 서버 간의 평균 지연시간을 보여줍니다.')
    async def ping(self, interaction):
        self.__logger.info(f"{interaction.guild.name}({interaction.guild.id})의 {interaction.channel.name}({interaction.channel.id})에서 '/핑' 사용")
        embed = discord.Embed(title=':ping_pong: 퐁!', description=f'지연시간: {round(self.__bot.latency * 1000)} ms',
                              color=0x711E92)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name='도움', description=f'봇의 명령어 목록과 설명을 보여줍니다.')
    async def help(self, interaction):
        self.__logger.info(f"{interaction.guild.name}({interaction.guild.id})의 {interaction.channel.name}({interaction.channel.id})에서 '/도움' 사용")
        embed = discord.Embed(title="봇 명령어 목록", color=0x711E92)
        embed.add_field(name=':warning:주의사항:warning:',
                        value='**봇 초대 후 `/알림설정` 명령어를 사용해야 학교 공지사항과 학사일정, 학식 알림을 받을 수 있습니다.**\n'
                              '학교 공지사항은 학교 홈페이지의 **대학공지사항, 학사공지, 장학공지, [선택]생활관공지**를 알려드립니다. '
                              '이외의 공지사항은 학교 홈페이지를 참고하시기 바랍니다.\n', inline=False)
        embed.add_field(name='`/2학 [날짜]`', value='제2학생회관의 오늘 식단을 보여줍니다. `[날짜]` 옵션으로 내일의 식단을 볼 수 있습니다.', inline=False)
        embed.add_field(name='`/테파`', value='테크노파크의 이번 주 식단표를 보여줍니다.', inline=False)
        embed.add_field(name='`/날씨`', value='현재 캠퍼스의 날씨와 1 ~ 6시간 뒤 날씨 예보를 보여줍니다.', inline=False)
        embed.add_field(name='`/핑`', value='명령어 입력 시점부터 메세지 전송까지 총 지연시간을 보여줍니다.', inline=False)
        embed.add_field(name='`/알림설정 [학식알림] [생활관공지알림]`',
                        value='알림을 설정하는 명령어입니다. 해당 명령어를 입력한 채널이 각종 알림을 받을 채널이 됩니다. (해당 명령어의 사용자는 관리자 권한이 있어야 합니다.)',
                        inline=False)
        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(Util(bot))
