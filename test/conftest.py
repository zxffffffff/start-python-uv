import sys
import pytest
from datetime import datetime

"""
scope 作用范围
- session 全局一次
- package 每个文件夹
- module 每个py文件
- class 每个测试类
- function 每个测试函数【默认】
"""

test_start_time = datetime.now()
test_case_call_outcome = {}  # 记录每个测试用例的成功/失败


def pytest_addoption(parser):
    parser.addoption(
        "--api-server-addr",
        action="store",
        default="http://localhost:5001",
        help="http服务地址",
    )
    parser.addoption(
        "--ai-langchain-addr",
        action="store",
        default="http://localhost:5002",
        help="http服务地址",
    )
    parser.addoption(
        "--ai-adk-addr",
        action="store",
        default="http://localhost:5003",
        help="http服务地址",
    )


@pytest.fixture(scope="session")
def api_server_addr(request):
    addr = request.config.getoption("--api-server-addr")
    assert addr.startswith("http")
    if addr.endswith("/"):
        addr = addr[:-1]
    yield addr


@pytest.fixture(scope="session")
def ai_langchain_addr(request):
    addr = request.config.getoption("--ai-langchain-addr")
    assert addr.startswith("http")
    if addr.endswith("/"):
        addr = addr[:-1]
    yield addr


@pytest.fixture(scope="session")
def ai_adk_addr(request):
    addr = request.config.getoption("--ai-adk-addr")
    assert addr.startswith("http")
    if addr.endswith("/"):
        addr = addr[:-1]
    yield addr


def pytest_runtest_logreport(report):
    """
    在每个测试项的每个阶段 (setup, call, teardown) 完成后调用
    """
    # 仅关心 call 阶段的成功/失败
    if report.when == "call":
        # print(f"pytest_runtest_logreport 触发 nodeid={report.nodeid} outcome={report.outcome}", flush=True)
        global test_case_call_outcome
        test_case_call_outcome[report.nodeid] = report.outcome

    sys.stdout.flush()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # 调用默认的钩子实现
    report = (yield).get_result()

    # 仅处理测试执行阶段（call）的失败
    if report.when == "call" and report.failed:
        # 获取堆栈信息字符串
        # if report.longreprtext.endswith("AssertionError"):
        #     print(report.longrepr)
        # else:
        print(Exception(report.longreprtext))

    sys.stdout.flush()


@pytest.fixture(scope="function")
def init_test_case(request):
    test_file = request.module.__file__
    test_case = request.function.__name__
    print(f"开始执行测试用例：{test_file}::{test_case}", flush=True)
