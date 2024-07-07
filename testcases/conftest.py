import pytest
import os
import allure
import json
from api.user import USER
from utils.logger import logger

BASE_PATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))


# # base_data = get_data_by_case_id("base_data.yml")
# #user_test_data = get_data_by_case_id(UserCaseData.get_all_data_by_sheet_name)
# # scenario_data = get_data_by_case_id("scenario_test_data.yml")


@allure.step("前置步骤 ==>> 清理数据")
def step_first():
    logger.info("******************************")
    logger.info("前置步骤开始 ==>> 清理数据")


@allure.step("后置步骤 ==>> 清理数据")
def step_last():
    logger.info("后置步骤开始 ==>> 清理数据")


# @allure.step("前置步骤 ==>> 管理员用户登录")
# def step_login(username, password):
#     logger.info("前置步骤 ==>> 管理员 {} 登录，返回信息 为：{}".format(username, password))
#
#
# @pytest.fixture(scope="session")
# def login_fixture():
#     username = base_data["init_admin_user"]["username"]
#     password = base_data["init_admin_user"]["password"]
#     header = {
#         "Content-Type": "application/x-www-form-urlencoded"
#     }
#     payload = {
#         "username": username,
#         "password": password
#     }
#     loginInfo = USER.login(data=payload, headers=header)
#     step_login(username, password)
#     yield loginInfo.json()
#
#
@pytest.fixture(scope="function")
def add_user_setup_down(request):
    _params: dict = request.node.callspec.params
    module, sub_module, domain, casename, pre_data, url, casemethod, expect_code, expect_result, note = _params.values()
    logger.info("start up")
    yield module, sub_module, domain, casename, pre_data, url, casemethod, expect_code, expect_result, note
    username = json.loads(pre_data).get("username")
    USER.del_users(username=username)
    logger.info("clear test data {}".format(username))

#
#
# @pytest.fixture(scope="function")
# def delete_register_user():
#     """注册用户前，先删除数据，用例执行之后，再次删除以清理数据"""
#     del_sql = base_data["init_sql"]["delete_register_user"]
#     db.execute_db(del_sql)
#     step_first()
#     logger.info("注册用户操作：清理用户--准备注册新用户")
#     logger.info("执行前置SQL：{}".format(del_sql))
#     yield
#     db.execute_db(del_sql)
#     step_last()
#     logger.info("注册用户操作：删除注册的用户")
#     logger.info("执行后置SQL：{}".format(del_sql))
#
#
# @pytest.fixture(scope="function")
# def update_user_telephone():
#     """修改用户前，因为手机号唯一，为了使用例重复执行，每次需要先修改手机号，再执行用例"""
#     update_sql = base_data["init_sql"]["update_user_telephone"]
#     db.execute_db(update_sql)
#     step_first()
#     logger.info("修改用户操作：手工修改用户的手机号，以便用例重复执行")
#     logger.info("执行SQL：{}".format(update_sql))
