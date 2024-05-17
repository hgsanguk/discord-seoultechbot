from abc import ABC, abstractmethod
from seoultechbot.model import DiscordServer


class DiscordServerRepository(ABC):
    """
    Discord 서버들의 설정을 관리하는 Repository의 추상 클래스입니다.

    Attributes:
        session: 데이터베이스를 조작하기 위한 세션, 클라이언트 등
    """
    def __init__(self, session):
        self.session = session

    @abstractmethod
    def get_by_id(self, server_id: int) -> DiscordServer:
        """
        주어진 id를 가진 Discord 서버의 SeoulTechBot 설정을 반환합니다.

        :param server_id: Discord 서버의 id
        :return: Discord 서버의 봇 설정(DiscordServer 객체)
        """
        raise NotImplementedError

    @abstractmethod
    def add(self, server: DiscordServer):
        """
        SeoulTechBot 데이터베이스에 새 Discord 서버를 추가합니다.

        :param server: Discord 서버의 봇 설정(DiscordServer 객체)
        """
        raise NotImplementedError

    @abstractmethod
    def update(self, server: DiscordServer) -> bool:
        """
        SeoulTechBot 데이터베이스에서 Discord 서버의 설정을 업데이트합니다.
        해당 Discord 서버가 데이터베이스에 존재하지 않을 경우 추가합니다.

        :param server: Discord 서버의 봇 설정(DiscordServer 객체)
        :return: 데이터베이스에 해당 Discord 서버의 존재 여부
        """
        raise NotImplementedError

    @abstractmethod
    async def delete(self, server_id: int) -> bool:
        """
        SeoulTechBot 데이터베이스에서 Discord 서버를 삭제합니다.

        :param server_id: Discord 서버의 id
        :return 데이터베이스에 해당 id의 Discord 서버 유무
        """
        raise NotImplementedError

    @abstractmethod
    def clear_channel_id(self, server_id: int, column_names: tuple[str] | list[str]) -> bool:
        """
        Discord 서버의 특정 Column들의 텍스트 채널 ID를 null(None)로 만듭니다.
        데이터베이스에 Discord 서버가 없을 경우 아무런 작업도 하지 않습니다.

        :param server_id: Discord 서버의 id
        :param column_names: 텍스트 채널 id를 제거할 Column 이름 리스트 혹은 목록
        :return: 데이터베이스에 해당 id의 Discord 서버 유무
        """
        raise NotImplementedError

    @abstractmethod
    def clear_channel_id_from_column(self, channel_id: int, column_name: str):
        """
        SeoulTechBot 데이터베이스에서 특정 Column의 텍스트 채널 ID를 찾아 null(None)로 만듭니다.

        :param channel_id: 텍스트 채널의 id
        :param column_name: 텍스트 채널 id를 제거할 Column 이름
        """
        raise NotImplementedError

    @abstractmethod
    def get_channel_id_cafeteria_menu_by_hour(self, notify_hour: int):
        """
        특정 학식 알림 시간을 설정한 Discord 서버의 텍스트 채널 id list를 반환합니다.

        :param notify_hour: 학식 알림 시간
        :return: 텍스트 채널 id 리스트 or 튜플
        """
        raise NotImplementedError

    @abstractmethod
    def get_channel_id_all_from_column(self, column_name: str):
        """
        특정 알림을 설정한 모든 Discord 서버의 텍스트 채널 id list를 반환합니다.
        알림을 설정하지 않은 경우(DB상 Null인 경우) list에 포함 시키지 않습니다.

        :param column_name: 텍스트 채널에 설정된 알림 종류에 대한 Column
        :return: 텍스트 채널 id 리스트 or 튜플
        """
        raise NotImplementedError

    @abstractmethod
    def get_channel_id_notice_dormitory_all(self):
        """
        기숙사 공지사항 알림을 받기로 설정한 모든 Discord 서버의 텍스트 채널 id list를 반환합니다.
        알림을 설정하지 않은 경우(DB상 Null인 경우) list에 포함 시키지 않습니다.

        :return: 텍스트 채널 id 리스트 or 튜플
        """
        raise NotImplementedError
