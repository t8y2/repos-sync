from enum import Enum


class UserStatus(Enum):
    ACCOUNT_FROZEN = (2000, "账户已被冻结")
    ACCOUNT_EXISTS = (2001, "账号已存在")
    ACCOUNT_NOT_EXISTS = (2002, "账号不存在")
    PASSWORD_ERROR = (2003, "密码错误")
    NOT_AUTHENTICATED = (2004, "未认证")

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
