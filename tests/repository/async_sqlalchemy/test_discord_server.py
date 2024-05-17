"""
DiscordServerRepository 클래스의 여러 메서드를 테스트하는 모듈입니다.
"""
import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from seoultechbot.model import Base, DiscordServer
from seoultechbot.repository.async_sqlalchemy import AsyncSqlAlchemyDiscordServerRepository


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
        discord_server_repo = AsyncSqlAlchemyDiscordServerRepository(session)

        # 서버 추가
        discord_server = DiscordServer(id=10001,
                                       cafeteria_menu_notify_time=-1,
                                       receive_dormitory_notice=False,
                                       channel_id_notice=100011,
                                       channel_id_cafeteria_menu=100012)
        discord_server_repo.add(discord_server)

        # 서버 정보 가져오기
        result = await discord_server_repo.get_by_id(discord_server.id)

        # 값이 같은지 확인
        assert result is not None
        assert result.channel_id_notice == 100011
        assert result.channel_id_cafeteria_menu == 100012
        assert result.cafeteria_menu_notify_time == -1
        assert result.receive_dormitory_notice is False

        # 없는 서버 정보 None 인지 확인
        result = await discord_server_repo.get_by_id(10002)
        assert result is None
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
        discord_server_repo = AsyncSqlAlchemyDiscordServerRepository(session)

        discord_server = DiscordServer(id=10001,
                                       cafeteria_menu_notify_time=-1,
                                       channel_id_notice=100011)
        discord_server_2nd = DiscordServer(id=10002,
                                           cafeteria_menu_notify_time=9,
                                           receive_dormitory_notice=True,
                                           channel_id_cafeteria_menu=100021,
                                           channel_id_notice=100022)
        discord_server_repo.add(discord_server)
        discord_server_repo.add(discord_server_2nd)

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

        # DB 업데이트 반영됐는지 검사
        exist_server = await discord_server_repo.update(discord_server)
        result = await discord_server_repo.get_by_id(discord_server.id)
        assert exist_server is True
        assert result is not None
        assert result.channel_id_notice == 100015
        assert result.channel_id_cafeteria_menu == 100013
        assert result.cafeteria_menu_notify_time == 9
        assert result.receive_dormitory_notice is True

        exist_server = await discord_server_repo.update(discord_server_2nd)
        result = await discord_server_repo.get_by_id(discord_server_2nd.id)
        assert exist_server is True
        assert result is not None
        assert result.channel_id_notice is None
        assert result.channel_id_cafeteria_menu is None
        assert result.cafeteria_menu_notify_time == -1
        assert result.receive_dormitory_notice is False

        # DB에 없는 서버 Update 시도
        discord_server_3rd = DiscordServer(id=10003,
                                           receive_dormitory_notice=True,
                                           channel_id_notice=100031)
        exist_server = await discord_server_repo.update(discord_server_3rd)
        result = await discord_server_repo.get_by_id(10003)
        assert result is not None
        assert exist_server is False
        assert result.channel_id_notice is 100031
        assert result.channel_id_cafeteria_menu is None
        assert result.cafeteria_menu_notify_time == -1
        assert result.receive_dormitory_notice is True
    await engine.dispose()


@pytest.mark.asyncio
async def test_delete():
    """
    데이터베이스에서 Discord 서버가 삭제되었는지 테스트합니다.
    """
    engine = create_async_engine('sqlite+aiosqlite:///:memory:', echo=True)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    AsyncSessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with AsyncSessionLocal() as session:
        discord_server_repo = AsyncSqlAlchemyDiscordServerRepository(session)

        discord_server = DiscordServer(id=10001,
                                       cafeteria_menu_notify_time=-1,
                                       channel_id_notice=100011)
        discord_server_2nd = DiscordServer(id=10002,
                                           cafeteria_menu_notify_time=9,
                                           receive_dormitory_notice=True,
                                           channel_id_cafeteria_menu=100021,
                                           channel_id_notice=100022)
        discord_server_repo.add(discord_server)
        discord_server_repo.add(discord_server_2nd)

        # 첫번째 디스코드 서버 삭제
        await discord_server_repo.delete(discord_server.id)

        # 삭제되었는지 체크
        result = await discord_server_repo.get_by_id(discord_server.id)
        assert result is None

        # 삭제 안 된건 잘 있는지 체크
        result = await discord_server_repo.get_by_id(discord_server_2nd.id)
        assert result is not None
        assert result.channel_id_notice is 100022
        assert result.channel_id_cafeteria_menu is 100021
        assert result.cafeteria_menu_notify_time == 9
        assert result.receive_dormitory_notice is True

        # 없는 서버 제거 시도
        result = await discord_server_repo.delete(10003)
        assert result is False
    await engine.dispose()


@pytest.mark.asyncio
async def test_clear_channel_id():
    """
    데이터베이스에서 사용자가 선택한 Channel ID가 제거되는지 테스트합니다.
    """
    engine = create_async_engine('sqlite+aiosqlite:///:memory:', echo=True)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    AsyncSessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with AsyncSessionLocal() as session:
        discord_server_repo = AsyncSqlAlchemyDiscordServerRepository(session)

        discord_server = DiscordServer(id=10001,
                                       cafeteria_menu_notify_time=-1,
                                       channel_id_cafeteria_menu=100012,
                                       channel_id_notice=100011)
        discord_server_2nd = DiscordServer(id=10002,
                                           cafeteria_menu_notify_time=9,
                                           receive_dormitory_notice=True,
                                           channel_id_cafeteria_menu=100021,
                                           channel_id_notice=100022)
        discord_server_repo.add(discord_server)
        discord_server_repo.add(discord_server_2nd)

        await discord_server_repo.clear_channel_id(discord_server.id, ('channel_id_notice', 'channel_id_cafeteria_menu'))
        await discord_server_repo.clear_channel_id(discord_server_2nd.id, ('channel_id_cafeteria_menu', ))

        result = await discord_server_repo.get_by_id(discord_server.id)
        assert result is not None
        assert result.channel_id_notice is None
        assert result.channel_id_cafeteria_menu is None

        result = await discord_server_repo.get_by_id(discord_server_2nd.id)
        assert result is not None
        assert result.channel_id_notice is not None
        assert result.channel_id_cafeteria_menu is None
    await engine.dispose()


@pytest.mark.asyncio
async def test_clear_channel_id_from_column():
    """
    데이터베이스에서 임의의 Column에 있는 Channel ID가 제거되는지 테스트합니다.
    """
    engine = create_async_engine('sqlite+aiosqlite:///:memory:', echo=True)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    AsyncSessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with AsyncSessionLocal() as session:
        discord_server_repo = AsyncSqlAlchemyDiscordServerRepository(session)

        discord_server = DiscordServer(id=10001,
                                       cafeteria_menu_notify_time=-1,
                                       channel_id_cafeteria_menu=100012,
                                       channel_id_notice=100011)
        discord_server_2nd = DiscordServer(id=10002,
                                           cafeteria_menu_notify_time=9,
                                           receive_dormitory_notice=True,
                                           channel_id_cafeteria_menu=100021,
                                           channel_id_notice=100022)
        discord_server_repo.add(discord_server)
        discord_server_repo.add(discord_server_2nd)

        # Discord 서버에서 알림 해제
        await discord_server_repo.clear_channel_id_from_column(discord_server.channel_id_notice, 'channel_id_notice')
        await discord_server_repo.clear_channel_id_from_column(discord_server_2nd.channel_id_cafeteria_menu,'channel_id_cafeteria_menu')

        # 채널 ID가 제거되었는지 체크
        result = await discord_server_repo.get_by_id(discord_server.id)
        assert result is not None
        assert result.channel_id_notice is None
        assert result.channel_id_cafeteria_menu is not None

        result = await discord_server_repo.get_by_id(discord_server_2nd.id)
        assert result is not None
        assert result.channel_id_notice is not None
        assert result.channel_id_cafeteria_menu is None
    await engine.dispose()


@pytest.mark.asyncio
async def test_get_channel_id_cafeteria_menu_by_hour():
    """
    데이터베이스에서 학식 알림 시간으로 텍스트 채널 id를 제대로 불러오는지 확인합니다.
    """
    engine = create_async_engine('sqlite+aiosqlite:///:memory:', echo=True)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    AsyncSessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with AsyncSessionLocal() as session:
        discord_server_repo = AsyncSqlAlchemyDiscordServerRepository(session)

        discord_server = DiscordServer(id=10001,
                                       cafeteria_menu_notify_time=-1,
                                       channel_id_notice=100011)
        discord_server_2nd = DiscordServer(id=10002,
                                           cafeteria_menu_notify_time=9,
                                           receive_dormitory_notice=True,
                                           channel_id_cafeteria_menu=100021,
                                           channel_id_notice=100022)
        discord_server_3rd = DiscordServer(id=10003,
                                           cafeteria_menu_notify_time=9,
                                           receive_dormitory_notice=True,
                                           channel_id_notice=100031,
                                           channel_id_cafeteria_menu=100032)
        discord_server_repo.add(discord_server)
        discord_server_repo.add(discord_server_2nd)
        discord_server_repo.add(discord_server_3rd)

        # 9시 알림 설정한 Discord 서버의 채널 ID 불러오기
        result = await discord_server_repo.get_channel_id_cafeteria_menu_by_hour(9)

        assert result is not None
        assert discord_server.channel_id_cafeteria_menu not in result
        assert discord_server_2nd.channel_id_cafeteria_menu in result
        assert discord_server_3rd.channel_id_cafeteria_menu in result
    await engine.dispose()

@pytest.mark.asyncio
async def test_get_channel_id_all_from_column():
    """
    데이터베이스에서 특정 Column으로 텍스트 채널 id 목록을 불러올 수 있는지 테스트합니다.
    """
    engine = create_async_engine('sqlite+aiosqlite:///:memory:', echo=True)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    AsyncSessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with AsyncSessionLocal() as session:
        discord_server_repo = AsyncSqlAlchemyDiscordServerRepository(session)

        # DB에 특정 알림을 설정한 서버가 없을 경우
        result = await discord_server_repo.get_channel_id_all_from_column('channel_id_notice')
        assert len(result) == 0

        discord_servers = [DiscordServer(id=10001, channel_id_notice=100011),
                           DiscordServer(id=10002, channel_id_notice=100022),
                           DiscordServer(id=10003, channel_id_notice=100031),
                           DiscordServer(id=10004, channel_id_notice=100041),
                           DiscordServer(id=10005)]
        for discord_server in discord_servers:
            discord_server_repo.add(discord_server)

        # DB에 특정 알림을 설정한 서버 불러오기
        result = await discord_server_repo.get_channel_id_all_from_column('channel_id_notice')

        for discord_server in discord_servers:
            if discord_server.channel_id_notice:
                assert discord_server.channel_id_notice in result
            else:
                assert discord_server.channel_id_notice not in result
    await engine.dispose()
