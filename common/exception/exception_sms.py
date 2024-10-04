from common.exception.exception_base import BaseCustomException
from common.response.code_sms import SMSStatus


class VerificationCodeError(BaseCustomException):
    def __init__(self, msg=None, status=SMSStatus.VERIFICATION_CODE_ERROR):
        super().__init__(msg, status)


class VerificationNotExist(BaseCustomException):
    def __init__(self, msg=None, status=SMSStatus.VERIFICATION_NOT_EXISTS):
        super().__init__(msg, status)


class VerificationSpeedLimit(BaseCustomException):
    def __init__(self, msg=None, status=SMSStatus.VERIFICATION_SPEED_LIMIT):
        super().__init__(msg, status)
