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

    DefHeader = {"Accept": "application/json, text/plain, */*"}

    DefHeaderSort = {value: index for index, value in
                     enumerate(['Host', 'host', 'Accept', 'Origin', 'Referer', 'Sec-GPC', 'Connection', 'User-Agent',
                                'Content-Type', 'Authorization', 'Sec-Fetch-Dest', 'Sec-Fetch-Mode', 'Sec-Fetch-Site',
                                'Accept-Encoding', 'Accept-Language'])}

    @staticmethod
    def get_def_cases_property():
        def_cases_property = ['Module', 'Sub_Module', 'Domain', 'CaseName', 'Pre_Data', 'URL', 'Method', 'Expect_code',
                              'Expect_result']
        return def_cases_property