"""
DiscordServerRepository 클래스의 여러 메서드를 테스트하는 모듈입니다.
"""
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


# @pytest.mark.usefixtures('setup_database')
@pytest.mark.asyncio
async def test_get_by_id():
    """
    봇의 설정을 데이터베이스로 저장하고, Discord의 서버 id로 봇의 설정을 잘 가져오는지 테스트합니다.
    """
    engine = create_async_engine('sqlite+aiosqlite:///:memory:', echo=True)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    AsyncSessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with AsyncSessionLocal() as session:
        discord_server_repo = DiscordServerRepository(session)

        # 서버 추가
        discord_server = DiscordServer(id=10001,
                                       cafeteria_menu_notify_time=-1,
                                       receive_dormitory_notice=False,
                                       channel_id_notice=100011,
                                       channel_id_cafeteria_menu=100012)
        await discord_server_repo.add(discord_server)

        # 서버 정보 가져오기
        result = await discord_server_repo.get_by_id(discord_server.id)

        # 값이 같은지 확인
        assert result is not None
        assert result.channel_id_notice == 100011
        assert result.channel_id_cafeteria_menu == 100012
        assert result.cafeteria_menu_notify_time == -1
        assert result.receive_dormitory_notice is False
    await engine.dispose()


@pytest.mark.asyncio
async def test_update():
    """
    봇의 설정이 제대로 수정되었는지 테스트합니다.
    """
    engine = create_async_engine('sqlite+aiosqlite:///:memory:', echo=True)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    AsyncSessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with AsyncSessionLocal() as session:
        discord_server_repo = DiscordServerRepository(session)

        discord_server = DiscordServer(id=10001,
                                       cafeteria_menu_notify_time=-1,
                                       channel_id_notice=100011)
        discord_server_2nd = DiscordServer(id=10002,
                                           cafeteria_menu_notify_time=9,
                                           receive_dormitory_notice=True,
                                           channel_id_cafeteria_menu=100021,
                                           channel_id_notice=100022)
        await discord_server_repo.add(discord_server)
        await discord_server_repo.add(discord_server_2nd)

        # 기숙사 알림 설정 및 학식 알림 설정, 공지 채널 변경
        discord_server = DiscordServer(id=10001,
                                       cafeteria_menu_notify_time=9,
                                       receive_dormitory_notice=True,
                                       channel_id_notice=100015,
                                       channel_id_cafeteria_menu=100013)
        # 기숙사 알림 설정 및 학식 알림, 공지 모두 해제
        discord_server_2nd = DiscordServer(id=10002,
                                           cafeteria_menu_notify_time=-1,
                                           receive_dormitory_notice=False,
                                           channel_id_cafeteria_menu=None,
                                           channel_id_notice=None)
        await discord_server_repo.update(discord_server)
        await discord_server_repo.update(discord_server_2nd)

        # DB 업데이트 반영됐는지 검사
        result = await discord_server_repo.get_by_id(discord_server.id)
        assert result is not None
        assert result.channel_id_notice == 100015
        assert result.channel_id_cafeteria_menu == 100013
        assert result.cafeteria_menu_notify_time == 9
        assert result.receive_dormitory_notice is True

        result_2nd = await discord_server_repo.get_by_id(discord_server_2nd.id)
        assert result_2nd is not None
        assert result_2nd.channel_id_notice == None
        assert result_2nd.channel_id_cafeteria_menu is None
        assert result_2nd.cafeteria_menu_notify_time == -1
        assert result_2nd.receive_dormitory_notice is False
    await engine.dispose()