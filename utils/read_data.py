import yaml
import os
import pandas as pd
from configparser import ConfigParser
from utils.logger import logger
from utils.common import init_data_info

SETTINGS = init_data_info.GetDefaultConfigPath.SETTINGS.value
BASEDATA = init_data_info.GetDefaultConfigPath.BASEDATA.value


class MyConfigParser(ConfigParser):
    __slots__ = ("_filepath", "_data")

    def __init__(self, filepath):
        super().__init__(self)
        if os.path.exists(filepath) is False:
            print("file is none")
            exit()
        self._filepath = filepath
        self._data = dict()

    @property
    def data_ini(self) -> dict:
        config_init = ConfigParser()
        config_init.optionxform = str
        config_init.read(self._filepath, encoding="utf-8")
        sections = config_init.sections()
        for section in sections:
            section_dict = dict()
            options = config_init.options(section)
            for option in options:
                section_dict[option] = config_init.get(section, option)
            self._data[section] = section_dict
        return self._data

    @property
    def data_yaml(self) -> dict:
        logger.info("加载 {} 文件......".format(self._filepath))
        with open(self._filepath, encoding='utf-8') as f:
            yml_generator = yaml.safe_load_all(f.read())
        self._data = [i for i in yml_generator][0]
        logger.info("读到数据 ==>>  {} ".format(self._data))
        return self._data


class ConfigReadINI():
    def __init__(self, filepath=SETTINGS):
        self.config = MyConfigParser(filepath).data_ini

    def get_element(self, section=None, option=None) -> any:
        # section, option = section.lower() if section else None, option.lower() if option else None
        if section is None and option is None:
            return self.config
        try:
            element = self.config[section][option] if option else self.config[section]
            return element
        except KeyError as e:
            logger.info("cannot find element {}".format(e))
            return None


class ConfigReadYML():
    def __init__(self, filepath=BASEDATA):
        self.config = MyConfigParser(filepath).data_yaml

    def get_element(self, *args) -> any:
        _args_len = len(args)
        _dict_tmp_all = self.config
        if _args_len != 0:
            for _ in range(0, _args_len):
                if args[_] in _dict_tmp_all.keys():
                    _dict_tmp = _dict_tmp_all.get(args[_])
                else:
                    logger.info(KeyError(f"{args[_]} is not found"))
                    exit()
                if isinstance(_dict_tmp, dict) and _ == _args_len - 1:
                    return _dict_tmp
                elif isinstance(_dict_tmp, dict) and _ < _args_len - 1:
                    _dict_tmp_all = _dict_tmp
                    continue
                elif isinstance(_dict_tmp, dict) is False and _ < _args_len - 1:
                    logger.info(ValueError(f"{args[_]} format is error"))
                    exit()
                else:
                    return _dict_tmp
        else:
            return self.config


class ConfigReadExcel():

    _is_instances = dict()

    def __new__(cls, filename, *args, **kwargs):
        _is_instance = cls.__name__ + filename
        if _is_instance in cls._is_instances.keys():
            return cls._is_instances.get(_is_instance)
        self = super(ConfigReadExcel, cls).__new__(cls)
        self.filename = filename
        self.workbook = pd.ExcelFile(self.filename)
        cls._is_instances.update({_is_instance: self})
        return self

    def get_data_by_sheet_name(self, sheet_name: str, key: dict):
        fd = self.workbook.parse(sheet_name=sheet_name)






ApiRootUrl = ConfigReadINI().get_element(section="host", option="api_root_url")
DefUsername = ConfigReadINI().get_element(section="host", option="default_username")
DefPwd = ConfigReadINI().get_element(section="host", option="default_password")
InitToken = ConfigReadINI().get_element(section="RequestInit", option="init_token")

if __name__ == '__main__':
    filepath1 = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "api_test_data.xlsx")
    yml_init = MyConfigParser(filepath1)
    yml1 = yml_init.data_excel
    print(type(yml1))
