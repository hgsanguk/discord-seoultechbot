import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from seoultechbot.model import Base
from seoultechbot.model import (SeoulTechnoparkCafeteriaMenu,
                                SecondStudentsUnionBuildingCafeteriaMenu,
                                UniversityNotice,
                                DiscordServer)
from seoultechbot.repository import DiscordServerRepository


@pytest.fixture
async def setup_database():  # session을 AsyncSession으로 못 넘겨서 작동하지 않음
    engine = create_async_engine('sqlite+aiosqlite:///:memory:', echo=True)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    AsyncSessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with AsyncSessionLocal() as session:
        yield session
    await engine.dispose()


@pytest.mark.asyncio
async def test_get_by_id():
    engine = create_async_engine('sqlite+aiosqlite:///:memory:', echo=True)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    AsyncSessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with AsyncSessionLocal() as session:
        discord_server_repo = DiscordServerRepository(session)
        discord_server = DiscordServer(id=10001,
                                       cafeteria_menu_notify_time=-1,
                                       receive_dormitory_notice=False,
                                       channel_id_notice=100002,
                                       channel_id_cafeteria_menu=100002)
        await discord_server_repo.add(discord_server)
        result = await discord_server_repo.get_by_id(discord_server.id)
        assert result is not None
        assert result.channel_id_notice == 100002
        assert result.channel_id_cafeteria_menu == 100002
        assert result.cafeteria_menu_notify_time == -1
        assert result.receive_dormitory_notice is False
    await engine.dispose()
