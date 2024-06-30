from enum import Enum, unique
import os


@unique
class GetDefaultConfigPath(Enum):
    def __str__(self):
        return self.value

    RootPath = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    SETTINGS = os.path.join(RootPath, "config", "setting.ini")
    BASEDATA = os.path.join(RootPath, 'config', 'base_data.yml')
    CASEADATA = os.path.join(RootPath, "data", "api_test_data.xlsx")


@unique
class GetNormalConfig(Enum):
    def __str__(self):
        return self.value

    DefHeader = {"Accept": "application/json, text/plain, */*",
                 'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2'}

    @staticmethod
    def get_def_cases_property():
        def_cases_property = ['Module', 'Sub_Module', 'Domain', 'CaseName', 'Pre_Data', 'URL', 'Method', 'Expect_code',
                              'Expect_result']
        return def_cases_property
