import requests
import json
from core.rest_client import RestClient
from utils.logger import logger
from utils.read_data import ApiRootUrl, DefPwd, DefUsername
from utils.read_data import UserCaseData, UserCaseDataHeader

data_row = UserCaseData.get_data_by_case_id("1.1.1")


class User(RestClient):
    __slots__ = ("username", "password")

    def __new__(cls, username=DefUsername, password=DefPwd, *args, **kwargs):
        self = super(User, cls).__new__(cls, api_root_url=ApiRootUrl, username=username, password=password,
                                        web_type="VMC",
                                        *args, **kwargs)
        return self

    def add_users(self, data=None, **kwargs) -> requests.Response:
        _data = data if isinstance(data, dict) else json.loads(data)
        user_data = json.dumps(_data)
        return self.post("/auth/users", data=user_data)

    def user_login(self, **kwargs):
        pass

    def del_users(self, username, **kwargs):
        return self.delete("/auth/users/{}".format(self.get_users(username=username)))

    def update_password(self, **kwargs):
        url = "/auth/users/api/password"
        data = {"username": "testtest", "name": "testtest", "password": "casa1234", "enabled": 1,
                "email": "11111111@qq.com",
                "group": "admin"}

    def update_info(self, **kwargs):
        url = "/auth/users/api/password"
        data = {"username": "testtest", "name": "testtest", "password": "casa1234", "enabled": 1,
                "email": "11111111@qq.com",
                "group": "admin"}

    def get_users(self, username=None, **kwargs) -> any:
        """
        if username is None, will return user's user id and return int type
        """
        _result = list(self.get("/auth/users", **kwargs).json())
        try:
            result = _result if username is None else [_user for _user in _result if _user.get("username") == username][
                0].get("id")
            return result
        except IndexError as e:
            logger.info("error user is not exist")


USER: User = User()

if __name__ == '__main__':

    result = USER.add_users(json.dumps(
        {"username": "auto_admin", "name": "auto_admin", "password": "casa1234", "enabled": 1,
         "email": "auto_admin@qq.com", "group": "admin"}))
    print("###########add finish################")
    username = "auto_admin"
    result_check = USER.get_users(username)
    print(result_check)
    USER.del_users("auto_admin")
    print("###########delete finish################")
