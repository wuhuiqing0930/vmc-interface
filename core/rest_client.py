import requests
from urllib.parse import urljoin
import json as complexjson
from utils.common import logger


class RestClient():

    _is_instances = dict()

    def __new__(cls, api_root_url, header=None, *args, **kwargs):
        _is_instance = cls.__name__ + api_root_url + header
        if _is_instance in cls._is_instances.keys():
            return cls._is_instances.get(_is_instance)
        self = super(RestClient, cls).__new__(cls)
        self.api_root_url = api_root_url
        self.session = requests.session()
        if header is not None:
            self._update_header(header)
        cls._is_instances.update({_is_instance, self})
        return self

    def _update_header(self, header):
        return self.session.headers.update(header)

    def _build_url(self, end_pointer):
        return urljoin(self.api_root_url, end_pointer)

    def request(self, method, end_pointer, *args, **kwargs):
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
    pass
