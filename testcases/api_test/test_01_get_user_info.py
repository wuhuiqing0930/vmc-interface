import pytest
import allure
import json
from api.user import USER
from utils.logger import logger
from utils.read_data import UserCaseData

data_row = UserCaseData.get_data_by_case_id("1.1.4")
data_row1 = UserCaseData.get_data_by_submodule("Create_user")

@allure.step("步骤1 ==>> 获取所有用户信息")
def step_1():
    logger.info("步骤1 ==>> 获取所有用户信息")


@allure.step("步骤1 ==>> 获取某个用户信息")
def step_2(username):
    logger.info("步骤1 ==>> 获取某个用户信息：{}".format(username))


@allure.severity(allure.severity_level.TRIVIAL)
@allure.epic("Smoke-F8.5")
@allure.feature("Users")
class TestGetUserInfo():
    """获取用户信息模块"""

    @allure.story("Add  Users")
    @pytest.mark.single
    @pytest.mark.parametrize(
        ('module', 'sub_module', 'domain', 'casename', 'pre_data', 'url', 'casemethod', 'expect_code', 'expect_result',
         'note'),
        data_row1)
    def test_add_user(self, add_user_setup_down, module, sub_module, domain, casename, pre_data, url, casemethod,
                      expect_code,
                      expect_result, note):
        allure.dynamic.title(casename)
        if note:
            allure.dynamic.issue(note)
        logger.info("*************** 开始执行用例 ***************")
        step_1()
        result = USER.add_users(pre_data)
        username = json.loads(pre_data).get("username")
        result_check = USER.get_users(username)
        logger.info("code ==>> 期望结果：， 实际结果：{}".format(result.status_code))
        assert result.status_code == expect_code
        if expect_code == 200:
            assert isinstance(result_check, int)
        else:
            print(result_check)
            assert result_check is None
        logger.info("*************** 结束执行用例!!! ***************")


if __name__ == '__main__':
    pytest.main(["-q", "-s", "test_01_get_user_info.py"])
