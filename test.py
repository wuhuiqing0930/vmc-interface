import pytest

data_row = [
    ('module1', 'sub_module1', 'domain1', 'case1', 'pre_data1', 'url1', 'casemethod1', 'expect_code1', 'expect_result1', 'note1'),
    ('module2', 'sub_module2', 'domain2', 'case2', 'pre_data2', 'url2', 'casemethod2', 'expect_code2', 'expect_result2', 'note2'),
    # Add more tuples as needed
]

@pytest.fixture(scope="function")
def add_user_setup_down(request):
    module, sub_module, domain, casename, pre_data, url, casemethod, expect_code, expect_result, note = request.param
    print(f"Setting up for test case: {casename}")
    # Perform setup actions here, if any
    yield
    # Teardown actions here, if any
    print(f"Tearing down after test case: {casename}")

@pytest.mark.parametrize(
    ('module', 'sub_module', 'domain', 'casename', 'pre_data', 'url', 'casemethod', 'expect_code', 'expect_result', 'note'),
    data_row,
    indirect=['add_user_setup_down']  # Indicate that add_user_setup_down is used indirectly
)
def test_add_user(add_user_setup_down, module, sub_module, domain, casename, pre_data, url, casemethod, expect_code, expect_result, note):
    print(f"Running test case: {casename}")
    # Perform your test logic here
    assert expect_code == '200'  # Replace with your assertion logic
