import json as complexjson
import warnings
import json
from urllib.parse import urljoin

import requests
from urllib3.exceptions import InsecureRequestWarning

from utils.common.init_data_info import GetNormalConfig
from utils.logger import logger
from utils.read_data import InitToken

warnings.filterwarnings('ignore', category=InsecureRequestWarning)

DefHeaders = GetNormalConfig.DefHeader.value
DefHeaderKey = GetNormalConfig.DefHeaderSort.value


def re_auth_token(func):
    def auth_wrapper(self: 'RestClient', *args, **kwargs):
        url = self._build_url("/oauth/token")
        data = {
            'refresh_token': self.refresh_token.split(" ")[1],
            'grant_type': 'refresh_token'
        }
        auth_result = self.session.post(url=url, data=data, verify=False)
        if auth_result.status_code == 200:
            self.access_token = self._build_token_data(auth_result.json().get("access_token"))
            self.refresh_token = self._build_token_data(auth_result.json().get("refresh_token"))
            logger.info("access_token expired, need refresh")
        else:
            self.access_token, self.refresh_token = self._build_token_data(
                self.init_token()[0]), self._build_token_data(
                self.init_token()[1])
            logger.info("refresh_token expired, need auto re-login ")

        return func(self, *args, **kwargs)

    return auth_wrapper


class RestClient():
    __slots__ = (
        "api_root_url", "header", "session", "access_token", "refresh_token", "username", "password", "web_type")
    _is_instances = dict()

    def __new__(cls, api_root_url: str, username=None, password=None, web_type=None,
                header: dict = DefHeaders, *args,
                **kwargs):
        _is_instance = cls.__name__ + api_root_url
        if _is_instance in cls._is_instances.keys():
            return cls._is_instances.get(_is_instance)
        self = super(RestClient, cls).__new__(cls)
        self.api_root_url = api_root_url
        self.header = header
        self.session = requests.session()
        self.username = username
        self.password = password
        self.web_type = web_type
        if self.web_type == "VMC":
            self.access_token = self._build_token_data(self.init_token()[0])
            self.refresh_token = self._build_token_data(self.init_token()[1])
        else:
            self.access_token = None
            self.refresh_token = None
        if self.header is not None:
            self.update_header(self.header)
        cls._is_instances.update({_is_instance: self})
        return self

    def init_token(self):
        url = r'/oauth/token'
        self.header.update(self._build_token(InitToken))
        data = {
            'username': self.username,
            'password': self.password,
            'scope': 'vnfm',
            'grant_type': 'password'
        }
        try:
            self.update_header(header=self.header)
            login_result = self.session.post(self._build_url(url), data, verify=False)
            if login_result.status_code == 200:
                login_result_data = login_result.json()
                return login_result_data.get("access_token"), login_result_data.get("refresh_token")
            else:
                logger.info("login error, make sure username and password is correct")
                print(login_result.status_code)
                exit()
        except requests.exceptions.InvalidURL as e:
            logger.info(e)
            exit()

    def update_header(self, header: dict):
        _key = header.keys()
        _key_sorted = sorted(_key, key=lambda _k: DefHeaderKey[_k])
        _header = {k: header.get(k) for k in _key_sorted}
        self.session.headers.update(_header)

    def _complete_header_content(self):
        pass

    def _build_url(self, end_pointer):
        return urljoin(self.api_root_url, end_pointer)

    @staticmethod
    def _build_token_data(token: str) -> str:
        _token = "".join(["Bearer", " ", token])
        return _token

    @staticmethod
    def _build_token(token: str) -> dict:
        _token = {"Authorization": token}
        return _token

    def request(self, method, end_pointer, *args, **kwargs):
        if self.web_type == "VMC":
            return self.request_vmc(method, end_pointer, *args, **kwargs)
        else:
            return self.request_normal(method, end_pointer, *args, **kwargs)

    @re_auth_token
    def request_vmc(self, method, end_pointer, *args, **kwargs) -> requests.Response:
        url = self._build_url(end_pointer)
        self.header.update(self._build_token(self.access_token))
        self.update_header(header=self.header)
        response = self.session.request(method, url, verify=False, *args, **kwargs)
        status_code = response.status_code
        self.request_log(url, method)
        return response

    def request_normal(self, method, end_pointer, *args, **kwargs) -> requests.Response:
        url = self._build_url(end_pointer)
        response = self.session.request(method, url, verify=False, *args, **kwargs)
        status_code = response.status_code
        self.request_log(url, method)
        return response

    def get(self, url, **kwargs):
        return self.request("GET", url, **kwargs)

    def post(self, url, data=None, json=None, **kwargs):
        return self.request("POST", url, data, json, **kwargs)

    def put(self, url, data=None, **kwargs):
        return self.request("PUT", url, data, **kwargs)

    def delete(self, url, **kwargs):
        return self.request("DELETE", url, **kwargs)

    def patch(self, url, data=None, **kwargs):
        return self.request("PATCH", url, data, **kwargs)

    def close(self):
        self.session.close()

    def request_log(self, url, method, data=None, json=None, params=None, headers=None, files=None, cookies=None,
                    **kwargs):
        logger.info("接口请求地址 ==>> {}".format(url))
        logger.info("接口请求方式 ==>> {}".format(method))
        # Python3中，json在做dumps操作时，会将中文转换成unicode编码，因此设置 ensure_ascii=False
        logger.info("接口请求头 ==>> {}".format(complexjson.dumps(headers, indent=4, ensure_ascii=False)))
        logger.info("接口请求 params 参数 ==>> {}".format(complexjson.dumps(params, indent=4, ensure_ascii=False)))
        logger.info("接口请求体 data 参数 ==>> {}".format(complexjson.dumps(data, indent=4, ensure_ascii=False)))
        logger.info("接口请求体 json 参数 ==>> {}".format(complexjson.dumps(json, indent=4, ensure_ascii=False)))
        logger.info("接口上传附件 files 参数 ==>> {}".format(files))
        logger.info("接口 cookies 参数 ==>> {}".format(complexjson.dumps(cookies, indent=4, ensure_ascii=False)))


if __name__ == '__main__':
    test = RestClient("https://[172:0:16::aa04]", "admin", "admin01", web_type="VMC")
    data = json.dumps({"username": "autoadmin", "password": "autoadminpassword", "scope": "vnfm", "grant_type": "password"})
    result = test.post(url="/auth/users", json=data)
    print(result.json(), result.status_code)
