# -*- coding: utf-8 -*-
"""
@File: get_path.py
@Desc: 获取项目根目录工具
"""


import os


def get_root_dir():
    """获取项目根目录"""
    path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    return path


print(get_root_dir())
