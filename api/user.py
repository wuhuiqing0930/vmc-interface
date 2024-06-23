import requests

from core.rest_client import RestClient
from utils.read_data import ApiRootUrl, DefPwd, DefUsername
from utils.logger import logger


class User(RestClient):
    __slots__ = ("username", "password")

    def __new__(cls, username=DefUsername, password=DefPwd, *args, **kwargs):
        self = super(User, cls).__new__(cls, api_root_url=ApiRootUrl, *args, **kwargs)
        self.username = username
        self.password = password
        return self

    def auth_cookie(self):
        logger.info("Check if username and password valid")
        data = {"username": "admin", "password": "admin01"}
        try:
            login_result = self.post("login", data=data)
            if login_result.status_code == 200:
                token = ""
            else:
                logger.info("error")
                exit()
        except requests.exceptions.InvalidURL as e:
            logger.info(e)
            exit()

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


# USER = User()


if __name__ == '__main__':
    user1 = User("https://www.baidu.com")
    user2 = User("https://www.baidu.com")
    print(user1, user2)
