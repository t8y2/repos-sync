from common.response.code_base import BaseStatus
from common.response import StatusEnum


class BaseCustomException(Exception):
    """
    自定义异常 基类
    """

    def __init__(self, msg: str, status: StatusEnum, data=None):
        self.status = status
        self.msg = msg
        self.data = data


class ClientError(BaseCustomException):
    """
    客户端错误
    """

    def __init__(self, msg=None, status=BaseStatus.CLIENT_ERROR):
        super().__init__(msg, status)


class MissParams(BaseCustomException):
    """
    缺少必要参数
    """

    def __init__(self, msg=None, status=BaseStatus.MISS_PARAMS):
        super().__init__(msg, status)


class Unauthorized(BaseCustomException):
    """
    未授权
    """

    def __init__(self, msg=None, status=BaseStatus.UNAUTHORIZED):
        super().__init__(msg, status)


class Forbidden(BaseCustomException):
    """
    禁止访问
    """

    def __init__(self, msg=None, status=BaseStatus.FORBIDDEN):
        super().__init__(msg, status)


class UnknownError(BaseCustomException):
    """
    服务器未知错误
    """

    def __init__(self, msg=None, status=BaseStatus.UNKNOWN_ERROR):
        super().__init__(msg, status)


class TooManyRequest(BaseCustomException):
    """
    请求过于频繁
    """

    def __init__(self, msg=None, status=BaseStatus.TOO_MANY_REQUEST):
        super().__init__(msg, status)


class ValidatorError(BaseCustomException):
    """
    客户端参数校验错误
    """

    def __init__(self, msg=None, status=BaseStatus.VALIDATOR_ERROR):
        super().__init__(msg, status)
