from enum import Enum


class BaseStatus(Enum):
    """
    业务状态码基类
    """
    SUCCESS = (0, "成功")

    CLIENT_ERROR = (1000, "客户端错误")
    MISS_PARAMS = (1001, "缺少必要参数")
    UNAUTHORIZED = (1002, "未授权")
    FORBIDDEN = (1003, "禁止访问")
    JSON_INVALID = (1004, "JSON格式错误")
    TOO_MANY_REQUEST = (1005, "请求过于频繁")
    VALIDATOR_ERROR = (1006, "客户端参数校验错误")
    UNKNOWN_ERROR = (1007, "服务器未知错误")
    HTTP_ERROR = (1008, "HTTP 异常")

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
