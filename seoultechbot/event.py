from itertools import cycle

from discord.ext import commands
from seoultechbot import Logger, SeoulTechBot


class Event(commands.Cog):
    """
    봇의 이벤트를 관리하는 클래스 입니다.
    """
    def __init__(self, bot):
        self.__bot = bot
        self.__logger = Logger.setup('seoultechbot.event')
        self.__logger.debug(f'{__name__} 모듈 초기화 완료')

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        """
        봇이 서버에 참여했을 때 발생하는 이벤트입니다.
        상단부터 메세지를 보낼 수 있는 채널을 찾아 초기 메세지를 전송하고, 봇이 참여 중인 서버의 갯수를 갱신합니다.
        :param guild: 초대된 서버의 정보
        """
        for channel in guild.text_channels:
            if channel.permissions_for(guild.me).send_messages:
                await channel.send(f':wave: 안녕하세요! 서울과학기술대학교 비공식 디스코드 봇, {self.__bot.user.name}을 이용해주셔서 감사합니다.\n'
                                   '`/도움` 명령어로 명령어의 목록을 확인하실 수 있습니다.')
                break
        self.__logger.info(f'{guild.name}({guild.id}) 서버에서 {self.__bot.user.name} 추가')
        SeoulTechBot.status = cycle(['도움말: /도움', f'{SeoulTechBot.VERSION}', f'{len(self.__bot.guilds)}개의 서버와 함께'])
        self.__logger.debug(f'봇의 상태 갱신 완료, {len(self.__bot.guilds)}개의 서버에서 봇 이용 중')

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        """
        봇이 서버에서 제거되었을 때 발생하는 이벤트입니다.
        봇이 참여 중인 서버의 갯수를 갱신합니다.
        :param guild: 제거된 서버의 정보
        """
        self.__logger.info(f'{guild.name}({guild.id}) 서버에서 {self.__bot.user.name} 제거')
        SeoulTechBot.status = cycle(['도움말: /도움', f'{SeoulTechBot.VERSION}', f'{len(self.__bot.guilds)}개의 서버와 함께'])
        self.__logger.debug(f'봇의 상태 갱신 완료, {len(self.__bot.guilds)}개의 서버에서 봇 이용 중')


async def setup(bot):
    await bot.add_cog(Event(bot))
