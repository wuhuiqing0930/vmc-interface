import requests
import json
from core.rest_client import RestClient
from utils.logger import logger
from utils.common.init_data_info import GetNormalConfig
from utils.read_data import ApiRootUrl, DefPwd, DefUsername


class User(RestClient):
    __slots__ = ("username", "password")

    def __new__(cls, username=DefUsername, password=DefPwd, *args, **kwargs):
        self = super(User, cls).__new__(cls, api_root_url=ApiRootUrl, *args, **kwargs)
        self.username = username
        self.password = password
        self._init_token()
        return self

    def list_all_users(self, **kwargs):
        return self.get("/users", **kwargs)

    def list_one_user(self, username, **kwargs):
        return self.get("/users/{}".format(username), **kwargs)

    def register(self, **kwargs):
        return self.post("/register", **kwargs)

    def login(self, **kwargs):
        return self.post("/login", **kwargs)

    def update(self, user_id, **kwargs):
        return self.put("/update/user/{}".format(user_id), **kwargs)

    def delete(self, name, **kwargs):
        return self.post("/delete/user/{}".format(name), **kwargs)

    def auto_auth(self):
        pass


USER = User()

if __name__ == '__main__':
    pass
# user1 = User()
# user1.auto_token()
# data = {
#     'username': 'admin',
#     'password': 'admin01',
#     'scope': 'vnfm',
#     'grant_type': 'password'
# }
# header = {"Accept": "application/json, text/plain, */*",
#           'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
#           'Authorization': "Basic dm5mbTo4YTU1OTFhOS05ZjMzLTQzMjQtYjM4Ny1lMTQ0OTY3OGU4ZDI="
#           }
# test = requests.session().request(method='POST', url="https://[172:0:16::aa04]/oauth/token", data=data,
#                                   headers=header)
