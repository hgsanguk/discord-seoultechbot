"""
봇에서 발생할 수 있는 예외를 모아놓은 모듈입니다.
"""


class AbnormalResultCodeFromOpenAPIException(Exception):
    def __init__(self, code: str, message: str):
        """
        공공데이터포털에서 적절하지 않은 응답 코드를 반환할 경우 사용하는 Exception입니다.

        :param code: 공공데이터포털 Open API 서버가 반환한 resultCode
        :param message: 공공데이터포털 Open API 서버가 반환한 resultMessage
        """
        super().__init__(f"응답 코드 {code}, {message}")