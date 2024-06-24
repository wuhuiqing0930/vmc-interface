import requests
import json
from core.rest_client import RestClient
from utils.read_data import ApiRootUrl, DefPwd, DefUsername, InitToken
from utils.logger import logger
from utils.common.init_data_info import GetNormalConfig


def re_auth(func):
    def auth(func):
        return func
    return auth

class User(RestClient):
    __slots__ = ("username", "password", "access_token", "refresh_token")

    def __new__(cls, username=DefUsername, password=DefPwd, *args, **kwargs):
        self = super(User, cls).__new__(cls, api_root_url=ApiRootUrl, *args, **kwargs)
        self.username = username
        self.password = password
        self.access_token = None
        self.refresh_token = None
        self._init_token()
        return self

    def _init_token(self):
        logger.info("Check if username and password valid")
        url = '/oauth/token'
        header = {'Authorization': InitToken}
        data = {
            'username': 'admin',
            'password': 'admin01',
            'scope': 'vnfm',
            'grant_type': 'password'
        }
        try:
            self.update_header(header=header)
            login_result = self.post(url=url, data=data)
            if login_result.status_code == 200:
                result = login_result.json()
                self.access_token = result.get("access_token")
                self.refresh_token = result.get("access_token")
            else:
                logger.info("login error")
                exit()
        except requests.exceptions.InvalidURL as e:
            logger.info(e)
            exit()

    @re_auth
    def refresh_token(self):
        pass


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
