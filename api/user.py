import requests
import json
from core.rest_client import RestClient
from utils.logger import logger
from utils.common.init_data_info import GetNormalConfig
from utils.read_data import ApiRootUrl, DefPwd, DefUsername


class User(RestClient):
    __slots__ = ("username", "password")

    def __new__(cls, username=DefUsername, password=DefPwd, *args, **kwargs):
        self = super(User, cls).__new__(cls, api_root_url=ApiRootUrl, username=username, password=password,
                                        web_type="VMC",
                                        *args, **kwargs)
        return self

    def add_users(self, **kwargs):
        pass

    def user_login(self, **kwargs):
        pass

    def del_users(self, **kwargs):
        pass

    def update_password(self, **kwargs):
        url = "/auth/users/api/password"
        data = {"username": "testtest", "name": "testtest", "password": "casa1234", "enabled": 1, "email": "11111111@qq.com",
         "group": "admin"}

    def check_user(self, **kwargs):
        return self.get("/auth/users", **kwargs)


USER = User()

if __name__ == '__main__':
    pass
