import yaml
import os
import typing
import pandas as pd
from configparser import ConfigParser
from utils.logger import logger
from utils.common import init_data_info

SETTINGS = init_data_info.GetDefaultConfigPath.SETTINGS.value
BASEDATA = init_data_info.GetDefaultConfigPath.BASEDATA.value
CASEADATA = init_data_info.GetDefaultConfigPath.CASEADATA.value
DefCasesProperty = init_data_info.GetNormalConfig.get_def_cases_property()
UNION = typing.Union


class MyConfigParser():
    __slots__ = ("_filepath", "_data")

    def __init__(self, filepath):
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
            return element.strip('"')
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
    __slots__ = ("filename", "workbook")
    _is_instances = dict()

    def __new__(cls, filename, *args, **kwargs):
        _is_instance = cls.__name__ + filename
        if _is_instance in cls._is_instances.keys():
            return cls._is_instances.get(_is_instance)
        self = super(ConfigReadExcel, cls).__new__(cls)
        self.filename = filename
        try:
            self.workbook = pd.ExcelFile(self.filename)
        except FileNotFoundError as e:
            logger.info("The file is not exist,Pls check".format(self.filename))
            exit()
        cls._is_instances.update({_is_instance: self})
        return self

    def file_close(self):
        self.workbook.close()


class ConfigReadExcelBySheet(ConfigReadExcel):
    __slots__ = ("sheet_name", "fd")

    def __new__(cls, filename, sheet_name, *args, **kwargs):
        self = super(ConfigReadExcelBySheet, cls).__new__(cls, filename=filename)
        self.sheet_name = sheet_name
        self.fd = self.workbook.parse(sheet_name=self.sheet_name)
        return self

    def check_file_header(self):
        _header = self.fd.columns.to_list()
        if _header == DefCasesProperty:
            header = map(lambda x: x.lower(), _header)
            return list(header)
        else:
            logger.info("cases property in file is unmatch, please check {}".format(self.filename))
            exit()

    @property
    def get_cases_rows(self):
        return self.fd.shape[0]

    @property
    def get_all_data_by_sheet_name(self) -> list:
        fd_list = self.fd.values.tolist()
        return fd_list

    def _get_data_rows(self, column_name, column_data) -> UNION[list, tuple]:
        data = self.fd[self.fd[column_name].str.startswith(column_data)]
        return data.values.tolist()

    def get_data_by_case_id(self, case_id: str, column_name="CaseName"):
        """
        input casa_id in CasaName. like "1.1.1" in "1.1.1_create_an_admin_user"
        """
        return self._get_data_rows(column_name=column_name, column_data="".join([case_id, "_"]))

    def get_data_by_submodule(self, submodule: str, column_name="Sub_Module") -> list:
        """
        input casa_id in CasaName. like "Create_user" in "1.1.1_create_an_admin_user"
        """
        return self._get_data_rows(column_name=column_name, column_data=submodule)

    def file_close(self):
        self.workbook.close()


ApiRootUrl = ConfigReadINI().get_element(section="host", option="api_root_url")
DefUsername = ConfigReadINI().get_element(section="host", option="default_username")
DefPwd = ConfigReadINI().get_element(section="host", option="default_password")
InitToken = ConfigReadINI().get_element(section="RequestInit", option="init_token")
UserCaseData: ConfigReadExcelBySheet = ConfigReadExcelBySheet(filename=CASEADATA, sheet_name="Users")
UserCaseDataHeader: list = UserCaseData.check_file_header()

if __name__ == '__main__':
    print(UserCaseDataHeader)
