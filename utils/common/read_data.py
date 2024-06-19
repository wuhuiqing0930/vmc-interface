import yaml
import os
from configparser import ConfigParser
from utils.common.logger import logger
from utils import init_data_info

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

    @property
    def data_excel(self):
        pass

    def optionxform(self, optionstr):
        return optionstr


class ConfigReadINI():
    def __init__(self, filepath=SETTINGS):
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


class ConfigReadXLXS():
    pass

# if __name__ == '__main__':
# filepath = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "config", "setting.ini")
# data_init = ConfigReadINI(filepath)
# mysqlhost = data_init.get_element(section="mysql")
# print(mysqlhost)

# filepath1 = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "base_data.yml")
# yml_init = ConfigReadYML(filepath1)
# yml1 = yml_init.get_element("init_sql", "insert_delete_user")
# print(yml1)
