# -*- coding: utf-8 -*-
"""
@File: test_home.py
@Desc: 首页模块测试用例
"""


import pytest
import time
import allure
import logging

from page.home_page import HomePage
from common.element import HomeElement


@pytest.fixture()
def open_home(launcher):
    """打开首页"""
    home_page = HomePage(launcher)
    home_page.skip_ad()
    return home_page


class TestHome:

    @allure.severity("blocker")
    def test_headline(self, open_home):
        """
        1、打开app，进入首页
        2、检查是否默认选中首页tab
        3、检查是否默认选中头条
        """
        home_page = open_home
        assert home_page.is_element_selected(HomeElement.home_tab)
        assert home_page.is_element_selected(HomeElement.headline_title)

    def test_pull_to_refresh(self, open_home):
        """
        1、打开app, 进入首页-头条栏目
        2、下拉刷新
        3、检查是否存在刷新提示文案
        4、检查页面内容有无变化
        """
        home_page = open_home
        time.sleep(2)
        page_content = home_page.current_page_content()
        home_page.pull_to_refresh()
        assert home_page.check_element_exist(HomeElement.pull_to_refresh_prompt)
        assert home_page.current_page_content() != page_content

    def test_picture_news_card(self, open_home):
        """
        1、打开app，进入首页-头条栏目
        2、检查是否存在单图封面新闻卡片
        3、检查是否存在多图封面新闻卡片
        """
        home_page = open_home
        assert home_page.is_exist_single_image_news_card()
        assert home_page.is_exist_multi_image_news_card()
