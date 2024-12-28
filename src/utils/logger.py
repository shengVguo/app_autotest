# -*- coding: utf-8 -*-
"""
@File: logger.py
@Desc: 日志器
"""


import logging

from utils.get_path import get_root_dir


def set_logger():
    logger = logging.getLogger("root")
    logger.setLevel(level="DEBUG")
    fmt = logging.Formatter(
        fmt="%(asctime)s %(levelname)-6s %(name)s:%(filename)-15s:%(lineno)d === %(message)s"
    )

    ch = logging.StreamHandler()
    ch.setLevel(level="DEBUG")
    ch.setFormatter(fmt=fmt)
    logger.addHandler(ch)

    fh = logging.FileHandler(get_root_dir() + "/log/app_test.log", "a+", encoding="utf-8")
    fh.setLevel(level="DEBUG")
    fh.setFormatter(fmt=fmt)
    logger.addHandler(fh)
    return logger


def set_other_logger():
    # 排除其他日志器日志干扰
    logging.getLogger("urllib3").setLevel(logging.ERROR)
    logging.getLogger("uiautomator2").setLevel(logging.ERROR)
