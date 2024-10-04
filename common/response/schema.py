from common.response.code_base import BaseStatus
from common.response import StatusEnum


class ResponseBase(object):

    @staticmethod
    async def success(*, status: StatusEnum = BaseStatus.SUCCESS, msg=None, data=None) -> dict:
        return {
            "code": status.code,
            "msg": msg if (msg is not None) else status.msg,
            "data": data if (data is not None) else None
        }

    @staticmethod
    async def fail(*, status: StatusEnum, msg=None, data=None) -> dict:
        return {
            "code": status.code,
            "msg": f"{status.msg} | {msg}" if (msg is not None) else status.msg,
            "data": data if (data is not None) else None
        }


responseBase = ResponseBase()
