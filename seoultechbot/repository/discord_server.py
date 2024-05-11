from sqlalchemy import select

from seoultechbot.model import DiscordServer


class DiscordServerRepository:
    def __init__(self, session):
        self.session = session

    async def get_by_id(self, id: int) -> DiscordServer:
        """
        주어진 id의 Discord 서버의 SeoulTechBot 설정을 반환합니다.
        :param id: Discord 서버의 id
        :return: Discord 서버의 봇 설정(DiscordServer 객체)
        """
        result = await self.session.execute(select(DiscordServer).where(DiscordServer.id == id))
        return result.scalars().first()

    async def add(self, server: DiscordServer):
        """
        SeoulTechBot 데이터베이스에 새 Discord 서버를 추가합니다.
        :param server: DiscordServer 객체
        """
        self.session.add(server)
        await self.session.commit()

    async def update(self, config: DiscordServer):
        """
        SeoulTechBot 데이터베이스에서 Discord 서버의 세부사항을 업데이트 합니다.
        :param config: Discord 서버의 봇 설정(DiscordServer 객체)
        """
        pass

    async def delete(self, server_id: int):
        """
        SeoulTechBot 데이터베이스에서 Discord 서버를 삭제합니다.
        :param server_id: Discord 서버의 id
        """
        pass

    async def get_channel_id_cafeteria_menu_by_hour(self, notify_hour: int) -> list[int]:
        """
        특정 학식 알림 시간을 설정한 Discord 서버의 텍스트 채널 id list를 반환합니다.
        :param notify_hour: 학식 알림 시간
        :return: 텍스트 채널 id 리스트
        """
        pass

    def get_channel_id_notice_all(self) -> list[int]:
        """
        대학공지사항 알림을 설정한 모든 Discord 서버의 텍스트 채널 id list를 반환합니다.
        :return: 텍스트 채널 id 리스트
        """
        pass
