from enum import Enum


class SMSStatus(Enum):
    VERIFICATION_CODE_ERROR = (3000, "验证码错误")
    VERIFICATION_NOT_EXISTS = (3001, "验证码不存在")
    VERIFICATION_SPEED_LIMIT = (3002, "频率过高，请稍后再试")

    @property
    def code(self):
        """
        获取错误码
        """
        return self.value[0]

    @property
    def msg(self):
        """
        获取错误码码信息
        """
        return self.value[1]
