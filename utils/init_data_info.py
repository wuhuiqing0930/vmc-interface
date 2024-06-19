from enum import Enum, unique
import os

from utils.common.read_data import ConfigReadINI


@unique
class GetDefaultConfigPath(Enum):
    def __str__(self):
        return self.value

    RootPath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    SETTINGS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "config", "setting.ini")
    BASEDATA = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'config', 'base_data.yml')


@unique
class GetNormalConfig(Enum):
    def __str__(self):
        return self.value

    ApiRootUrl = ConfigReadINI().get_element(section="host", option="api_root_url")
