from fastapi import FastAPI, Request, status
from starlette.responses import JSONResponse
from common.response.schema import responseBase
from common.response.code_base import BaseStatus
from common.exception.exception_base import BaseCustomException
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException
from logger.logger import log
import traceback


def register_exception(app: FastAPI):
    @app.exception_handler(RequestValidationError)
    async def request_validation_error(request: Request, exc: RequestValidationError):
        """
        覆盖 fastapi 默认行为, 参数验证错误
        """
        response_status = BaseStatus.CLIENT_ERROR
        error = exc.errors()[0]
        msg = error["msg"]

        if error["type"] == "missing":
            response_status = BaseStatus.MISS_PARAMS
            msg = ",".join([item for item in error["loc"] if item != "body"])

        if error["type"] == "json_invalid":
            response_status = BaseStatus.JSON_INVALID
            msg = None

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=await responseBase.fail(status=response_status, msg=msg)
        )

    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        """
        覆盖 fastapi 默认行为, HTTP 异常
        """
        response_status = BaseStatus.HTTP_ERROR
        msg = exc.detail

        if exc.status_code == 401:
            response_status = BaseStatus.UNAUTHORIZED
            msg = None

        if exc.status_code == 403:
            response_status = BaseStatus.UNAUTHORIZED
            msg = None

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=await responseBase.fail(status=response_status, msg=msg)
        )

    @app.exception_handler(BaseCustomException)
    async def custom_exception_handler(request: Request, exc: BaseCustomException):
        """
        自定义异常
        :param request:
        :param exc:
        :return:
        """

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=await responseBase.fail(status=exc.status, msg=exc.msg, data=exc.data),
        )

    @app.exception_handler(Exception)
    async def all_exception_handler(request: Request, exc: Exception):
        """
        未知服务器异常
        """

        try:
            raise exc
        except Exception as e:
            log.error(traceback.format_exc())

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=await responseBase.fail(status=BaseStatus.UNKNOWN_ERROR, msg=str(exc)),
        )
