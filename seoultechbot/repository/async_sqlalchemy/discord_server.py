import logging

from sqlalchemy import select, delete, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from seoultechbot.model import DiscordServer
from seoultechbot.repository.base import DiscordServerRepository

logger = logging.getLogger(__name__)


class AsyncSqlAlchemyDiscordServerRepository(DiscordServerRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def get_by_id(self, server_id: int) -> DiscordServer:
        result = await self.session.execute(select(DiscordServer).filter_by(id=server_id))
        return result.scalar_one_or_none()

    def add(self, server: DiscordServer) -> bool:
        try:
            self.session.add(server)
            return True
        except Exception as e:
            logger.exception(e)
            return False

    async def update(self, server: DiscordServer) -> bool:
        target_server = await self.get_by_id(server.id)
        try:
            if target_server:
                server_dict = server.__dict__  # 서버에서 업데이트한 설정
                server_dict.pop('_sa_instance_state')  # sqlalchemy가 부여한 고유 id는 유지
                for key, value in server_dict.items():
                    if hasattr(target_server, key):  # 설정한 값이 있을 경우 교체, 없을 경우 유지
                        setattr(target_server, key, value)
                await self.session.flush()  # session.dirty == True로 만들어서 변경사항 반영
            else:
                self.add(server)
            return True
        except Exception as e:
            logger.exception(e)
            return False

    async def delete(self, server_id: int) -> bool:
        try:
            await self.session.execute(delete(DiscordServer).filter_by(id=server_id))
            return True
        except Exception as e:
            logger.exception(e)
            return False

    async def clear_channel_id(self, server_id: int, column_names: tuple) -> bool:
        target_server = await self.get_by_id(server_id)
        if target_server:
            for column in column_names:
                setattr(target_server, column, None)
            try:
                await self.session.flush()  # session.dirty == True로 만들어서 변경사항 반영
                return True
            except Exception as e:
                logger.exception(e)
                return False
        else:
            return False

    async def clear_channel_id_from_column(self, channel_id: int, column_name: str) -> bool:
        try:
            if 'channel_id' not in column_name:
                raise ValueError('column_name은 "channel_id"를 포함해야 합니다.')
            column = getattr(DiscordServer, column_name)
            await self.session.execute(update(DiscordServer).where(column == channel_id).values({column: None}))
            return True
        except Exception as e:
            logger.exception(e)
            return False

    async def get_channel_id_cafeteria_menu_by_hour(self, notify_hour: int):
        result = await self.session.execute(select(DiscordServer.channel_id_cafeteria_menu)
                                            .filter_by(cafeteria_menu_notify_time=notify_hour)
                                            .filter(DiscordServer.channel_id_cafeteria_menu.is_not(None)))
        return result.scalars().all()

    async def get_channel_id_all_from_column(self, column_name: str):
        if 'channel_id' not in column_name:
            raise ValueError('column_name은 "channel_id"를 포함해야 합니다.')
        column = getattr(DiscordServer, column_name)
        result = await self.session.execute(select(column).filter(column.is_not(None)))
        return result.scalars().all()
