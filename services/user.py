import hashlib
from datetime import datetime
from typing import List
from uuid import uuid4
from common.exception.exception_user import AccountExist, AccountNotExist, PassWordError
from dao.role import RoleDao
from dao.user import UserDao
from schemas.jwt import UserInfo
from schemas.user import DataBaseCreateUser, HttpCreateUser, HttpLogin
from services.jwt import JwtService


class UserService(object):
    @classmethod
    def generate_password_md5(cls, password):
        md5 = hashlib.md5()
        md5.update(password.encode("utf8"))
        return md5.hexdigest()

    @classmethod
    async def login(cls, obj: HttpLogin):
        user = await UserDao.get_by_username(obj.username)
        if user is None:
            raise AccountNotExist(obj.username)
        if cls.generate_password_md5(obj.password) != user["password"]:
            raise PassWordError()
        return JwtService.create_access_token(user["uid"], obj.username)

    @classmethod
    async def create_user(cls, obj: HttpCreateUser):
        user = await UserDao.get_by_username(obj.username)
        if user:
            raise AccountExist("用户名已存在")
        obj.password = cls.generate_password_md5(obj.password)

        # 创建用户
        await UserDao.create_user(DataBaseCreateUser(
            **obj.model_dump(),
            uid=str(uuid4()),
            last_login=datetime.now(),
        ))

    @classmethod
    async def list_user(cls):
        return await UserDao.list_user()

    @classmethod
    async def get_menus(cls, roles: List[str]) -> List[dict]:
        resp = await UserDao.get_menus(roles)
        return resp


