import requests
from urllib.parse import urljoin
import json as complexjson
from utils.logger import logger
from utils.common.init_data_info import GetNormalConfig
from utils.read_data import InitToken


def re_auth_token(func):
    def auth_wrapper(self: RestClient, *args, **kwargs):
        header = {'Authorization': self.refresh_token}
        url = "/oauth/token"
        data = ""
        auth_result = self.session.post(url=url, data=data, header=header)
        if auth_result.status_code == 200:
            new_access_token = {"Authorization": auth_result.json().get("refresh_token")}
            self.update_header(new_access_token)
            self.refresh_token = new_access_token
        else:  # 需更新
            new_access_token, new_refresh_token = self.init_token()[0], self.init_token()[1]
            self.update_header(new_refresh_token)
            self.access_token = new_access_token
            self.refresh_token = new_refresh_token
        logger.info("token expired, need refresh")
        return func(self, *args, **kwargs)

    return auth_wrapper


class RestClient():
    __slots__ = ("api_root_url", "session", "access_token", "refresh_token", "username", "password", "web_type")
    _is_instances = dict()

    def __new__(cls, api_root_url: str, username=None, password=None, web_type=None,
                header=GetNormalConfig.DefHeader.value, *args,
                **kwargs):
        _is_instance = cls.__name__ + api_root_url
        if _is_instance in cls._is_instances.keys():
            return cls._is_instances.get(_is_instance)
        self = super(RestClient, cls).__new__(cls)
        self.api_root_url = api_root_url
        self.session = requests.session()
        self.username = username
        self.password = password
        self.web_type = web_type
        if self.web_type == "VMC":
            self.access_token = self.init_token()[0]
            self.refresh_token = self.init_token()[1]
        else:
            self.access_token = None
            self.refresh_token = None
        if header is not None:
            self.update_header(header)
        cls._is_instances.update({_is_instance: self})
        return self

    def init_token(self):
        logger.info("Check if username and password valid")
        url = r'/oauth/token'
        header = {'Authorization': InitToken}
        data = {
            'username': self.username,
            'password': self.password,
            'scope': 'vnfm',
            'grant_type': 'password'
        }
        try:
            self.update_header(header=header)
            login_result = self.post(url=url, data=data)
            if login_result.status_code == 200:
                login_result = login_result.json()
                return login_result.get("access_token"), login_result.get("refresh_token")
            else:
                logger.info("login error, make sure username and password is correct")
                exit()
        except requests.exceptions.InvalidURL as e:
            logger.info(e)
            exit()

    def update_header(self, header):
        self.session.headers.update(header)

    def _build_url(self, end_pointer):
        return urljoin(self.api_root_url, end_pointer)

    def request(self, method, end_pointer, *args, **kwargs):
        if self.web_type == "VMC":
            return self.request_vmc(self, method, end_pointer, *args, **kwargs)
        else:
            return self.request_normal(self, method, end_pointer, *args, **kwargs)

    #@re_auth_token
    def request_vmc(self, method, end_pointer, *args, **kwargs) -> requests.Response:
        url = self._build_url(end_pointer)
        response = self.session.request(method=method, url=url, verify=False, *args, **kwargs)
        status_code = response.status_code
        self.request_log(url, method)
        return response

    def request_normal(self, method, end_pointer, *args, **kwargs) -> requests.Response:
        url = self._build_url(end_pointer)
        response = self.session.request(method=method, url=url, verify=False, *args, **kwargs)
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
    test = RestClient("https://[172:0:16::aa04]", "admin", "admin01")
    data = test.init_token()
