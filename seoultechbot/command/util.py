# Discord 명령 전송을 위한 패키지
import discord
from discord import app_commands
from discord.ext import commands

# 로거 설정을 위한 라이브러리
import logging

from seoultechbot import __version__, SeoulTechBot
from seoultechbot.repository.async_sqlalchemy import AsyncSqlAlchemyDiscordServerRepository


class Util(commands.Cog):
    """
    봇의 작동과 사용에 유용한 명령어를 모아놓은 클래스입니다.
    """
    def __init__(self, bot: SeoulTechBot):
        self.__logger = logging.getLogger(__name__)
        self.__bot = bot
        self.__logger.debug(f'{__name__} 모듈 초기화 완료')
        self.__repository = AsyncSqlAlchemyDiscordServerRepository(self.__bot.db_session)

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
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(name='정보', description="서버에서 받는 알림의 종류와 봇의 정보를 보여줍니다.")
    async def info(self, interaction: discord.Interaction):
        self.__logger.info(f"{interaction.guild.name}({interaction.guild.id})의 {interaction.channel.name}({interaction.channel.id})에서 '/정보' 사용")
        embed = discord.Embed(title="봇 정보",
                              description=f'discord.py 버전: `{discord.__version__}`\n'
                                          f'SeoulTechBot 버전: `{__version__}`\n'
                                          f'봇 이름: `{self.__bot.user.name}#{self.__bot.user.discriminator}`\n'
                                          f'날씨 기능: `{self.__bot.enable_weather_command}`\n'
                                          f'대학공지사항 스크래핑 주기: `{self.__bot.config.scrap_period}초`',
                              color=0x711E92)
        embed.set_thumbnail(url=self.__bot.user.avatar)

        # 서버 정보 불러오기
        server = await self.__repository.get_by_id(interaction.guild.id)
        none_str = "알림을 설정하지 않았습니다."
        notice_count = 0
        if server:
            # 학식 알림
            channel_cafeteria_menu = self.__bot.get_channel(server.channel_id_cafeteria_menu)
            notice_count += 1 if channel_cafeteria_menu else 0
            cafeteria_str = f"채널 이름: `{channel_cafeteria_menu.name}`\n알림 시간: `{server.cafeteria_menu_notify_time}시`"

            # 학교 공지사항
            channel_notice = self.__bot.get_channel(server.channel_id_notice)
            notice_count += 1 if channel_notice else 0
            notice_str = f"채널 이름: `{channel_notice.name}`\n기숙사 공지사항 알림: `{server.receive_dormitory_notice}`"

            # 정보 표시
            if notice_count > 0:
                embed.add_field(name=f"`{interaction.guild.name}` 서버의 알림 설정 정보",
                                value=f"총 {notice_count}개의 알림을 수신 중입니다.", inline=False)
                embed.add_field(name="🍽️ 식당 메뉴", value=cafeteria_str if channel_cafeteria_menu else none_str)
                embed.add_field(name="🏫 대학교 공지사항 및 학사일정", value=notice_str if channel_notice else none_str)
            else:
                embed.add_field(name=f"`{interaction.guild.name}` 서버의 알림 설정 정보", value=f"서버에서 {none_str}", inline=False)
        else:
            embed.add_field(name=f"`{interaction.guild.name}` 서버의 알림 설정 정보", value=f"서버에서 {none_str}", inline=False)

        await interaction.response.send_message(embed=embed, ephemeral=True)


async def setup(bot):
    await bot.add_cog(Util(bot))
