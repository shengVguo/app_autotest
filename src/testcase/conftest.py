# -*- coding: utf-8 -*-
"""
@File: conftest.py
@Desc: 全局前置后置，钩子函数等
"""


import pytest
import time
import logging

from common.app import App
from utils.logger import set_logger, set_other_logger


SERIAL = "127.0.0.1:7555"
app = App()


@pytest.fixture()
def launcher():
    """启动和退出app"""
    logging.info("***************启动app****************")
    device = app.start()
    yield device
    logging.info("***************关闭app****************")
    app.stop()


@pytest.fixture(autouse=True, scope="function")
def function_log_and_set_case_info(request):
    case_name = request.node.name
    logging.info("**************开始执行：{}***************".format(case_name))
    yield
    logging.info("**************结束执行：{}***************".format(case_name))


def pytest_collection_modifyitems(items):
    for item in items:
        item.name = item.name.encode("utf-8").decode("unicode-escape")
        item._nodeid = item.nodeid.encode("utf-8").decode("unicode-escape")


def pytest_runtest_call(item):
    docstring = item.obj.__doc__
    if docstring:
        logging.info(f"【测试步骤】：\n{docstring}")


def pytest_terminal_summary(terminalreporter, exitstatus, config):
    """收集测试结果"""
    print("===============pytest_terminal_summary===================")
    result = {
        "total": terminalreporter._numcollected,
        "passed": len(terminalreporter.stats.get("passed", [])),
        "failed": len(terminalreporter.stats.get("failed", [])),
        "error": len(terminalreporter.stats.get("error", [])),
        "skipped": len(terminalreporter.stats.get("skipped", [])),
    }
    print("total:", result["total"])
    print("passed:", result["passed"])
    print("failed:", result["failed"])
    print("error:", result["error"])
    print("skipped:", result["skipped"])

    duration = time.time() - terminalreporter._sessionstarttime
    print("total times:", duration, "seconds")


def pytest_configure(config):
    """配置日志"""
    set_logger()
    set_other_logger()
