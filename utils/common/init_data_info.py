from enum import Enum, unique
import os


@unique
class GetDefaultConfigPath(Enum):
    def __str__(self):
        return self.value

    RootPath = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    SETTINGS = os.path.join(RootPath, "config", "setting.ini")
    BASEDATA = os.path.join(RootPath, 'config', 'base_data.yml')


@unique
class GetNormalConfig(Enum):
    def __str__(self):
        return self.value

    DefHeader = {"Accept": "application/json, text/plain, */*"}

