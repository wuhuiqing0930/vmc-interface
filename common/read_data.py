import yaml
import json
from configparser import ConfigParser
from common.logger import logger

import os
import sys

SETTINGS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "config", "setting.ini")


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
        self._data =
        logger.info("读到数据 ==>>  {} ".format(self._data))
        return self._data

    @property
    def data_excel(self):
        pass


    def optionxform(self, optionstr):
        return optionstr




class ConfigReadINI():
    def __init__(self, filepath):
        self.config = MyConfigParser(filepath).data_ini

    def get_element(self, section, option=None) -> any:
        section, option = section.lower() if section else None, option.lower() if option else None
        try:
            element = self.config[section][option] if option else self.config[section]
            return element
        except KeyError as e:
            logger.info("cannot find element {}".format(e))
            return None


class ConfigReadYML():
    def __init__(self, filepath):
        self.config = MyConfigParser(filepath).data_yaml

    def get_element(self, section, option=None) -> any:
        section, option = section.lower() if section else None, option.lower() if option else None
        try:
            element = self.config[section][option] if option else self.config[section]
            return element
        except KeyError as e:
            logger.info("cannot find element {}".format(e))
            return None



# class ReadFileData():
#
#     def __init__(self):
#         pass
#
#     def load_yaml(self, file_path):
#         logger.info("加载 {} 文件......".format(file_path))
#         with open(file_path, encoding='utf-8') as f:
#             data = yaml.safe_load(f)
#         logger.info("读到数据 ==>>  {} ".format(data))
#         return data
#
#     def load_json(self, file_path):
#         logger.info("加载 {} 文件......".format(file_path))
#         with open(file_path, encoding='utf-8') as f:
#             data = json.load(f)
#         logger.info("读到数据 ==>>  {} ".format(data))
#         return data


if __name__ == '__main__':
    # filepath = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "config", "setting.ini")
    # data_init = ConfigReadINI(filepath)
    # mysqlhost = data_init.get_element(section="mysql")
    # print(mysqlhost)

    filepath1 = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "api_test_data.yml")
    yml_init = MyConfigParser(filepath1).data_yaml
    print(type(yml_init))
