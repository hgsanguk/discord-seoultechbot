# Discord 명령 전송을 위한 패키지
import discord
from discord import app_commands
from discord.ext import commands

# 로거 설정을 위한 라이브러리
import logging

from seoultechbot import __version__, SeoulTechBot, Config


class Util(commands.Cog):
    """
    봇의 작동과 사용에 유용한 명령어를 모아놓은 클래스입니다.
    """
    def __init__(self, bot: SeoulTechBot):
        self.__logger = logging.getLogger(__name__)
        self.__bot = bot
        self.__logger.debug(f'{__name__} 모듈 초기화 완료')

    @app_commands.command(name='핑', description="봇과 Discord 서버 간의 평균 지연시간을 보여줍니다.")
    async def ping(self, interaction: discord.Interaction):
        self.__logger.info(f"{interaction.guild.name}({interaction.guild.id})의 {interaction.channel.name}({interaction.channel.id})에서 '/핑' 사용")
        embed = discord.Embed(title=':ping_pong: 퐁!', description=f'지연시간: {round(self.__bot.latency * 1000)} ms', color=0x711E92)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name='도움', description="봇의 명령어 목록과 설명을 보여줍니다.")
    async def help(self, interaction: discord.Interaction):
        self.__logger.info(f"{interaction.guild.name}({interaction.guild.id})의 {interaction.channel.name}({interaction.channel.id})에서 '/도움' 사용")
        embed = discord.Embed(title="봇 명령어 목록", color=0x711E92)
        embed.add_field(name=':warning:주의사항:warning:',
                        value='**봇 초대 후 `/설정` 명령어를 사용해야 각종 알림을 받을 수 있습니다.**\n'
                              '현재 학교 공지사항은 학교 홈페이지의 **대학공지사항, 학사공지, 장학공지, [선택]생활관공지**를 알려드립니다. '
                              '이외의 공지사항은 학교 홈페이지를 참고하시기 바랍니다.\n', inline=False)
        # 명령어 목록 가져와서 embed 생성
        commands = self.__bot.tree.get_commands()
        for command in commands:
            parameters_str = ''
            for parameter in command.parameters:
                parameters_str += f" [{parameter.name}]"
            embed.add_field(name=f"`/{command.name}{parameters_str}`", value=command.description, inline=False)
        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(Util(bot))
