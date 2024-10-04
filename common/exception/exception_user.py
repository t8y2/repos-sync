from common.exception.exception_base import BaseCustomException
from common.response.code_user import UserStatus


class AccountExist(BaseCustomException):
    def __init__(self, msg=None, status=UserStatus.ACCOUNT_EXISTS):
        super().__init__(msg, status)


class AccountNotExist(BaseCustomException):
    def __init__(self, msg=None, status=UserStatus.ACCOUNT_NOT_EXISTS):
        super().__init__(msg, status)


class PassWordError(BaseCustomException):
    def __init__(self, msg=None, status=UserStatus.PASSWORD_ERROR):
        super().__init__(msg, status)
