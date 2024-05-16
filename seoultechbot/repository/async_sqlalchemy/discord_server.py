from abc import ABC, abstractmethod

from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from seoultechbot.model import DiscordServer
from seoultechbot.repository.base import DiscordServerRepository


class AsyncSqlAlchemyDiscordServerRepository(DiscordServerRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, id: int) -> DiscordServer:
        result = await self.session.execute(select(DiscordServer).filter_by(id=id))
        return result.scalar_one_or_none()

    async def add(self, server: DiscordServer):
        self.session.add(server)

    async def update(self, server: DiscordServer):
        server_dict = server.__dict__
        server_dict.pop('_sa_instance_state')  # sqlalchemy가 부여한 고유 id는 유지
        target_server = await self.get_by_id(server.id)
        if target_server:
            for key, value in server_dict.items():
                if hasattr(target_server, key):
                    setattr(target_server, key, value)
        await self.session.flush()  # session.dirty == True로 만들어서 변경사항 반영

    async def delete(self, server_id: int):
        pass

    async def get_channel_id_cafeteria_menu_by_hour(self, notify_hour: int) -> list[int]:
        pass

    def get_channel_id_notice_all(self) -> list[int]:
        pass
