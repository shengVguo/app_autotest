# -*- coding: utf-8 -*-
"""
@File: test_comment.py
@Desc: 跟帖模块测试用例
"""


import time
import pytest

from page.news_page import NewsPage
from page.home_page import HomePage
from common.element import HomeElement, NewsElement


@pytest.fixture()
def open_graphic_news_page(launcher):
    """进入图文新闻页"""
    home_page = HomePage(launcher)
    home_page.skip_ad()
    return home_page.go_to_news_page()


class TestNews:
    def test_graphic_news(self, open_graphic_news_page):
        """
        1、进入图文新闻页
        2、查看新闻详情页元素
        """
        news_page = open_graphic_news_page
        assert news_page.check_element_exist(NewsElement.news_title)
        assert news_page.check_element_exist(NewsElement.author_info)

    def test_follow_author(self, open_graphic_news_page):
        """
        1、进入图文新闻页
        2、关注作者，观察按钮变化
        3、取消关注，观察按钮变化
        """
        news_page = open_graphic_news_page
        news_page.click_element(NewsElement.follow_btn)
        assert news_page.check_element_exist(NewsElement.unsupport_btn)
        news_page.click_element(NewsElement.unsupport_btn)
        assert news_page.check_element_exist(NewsElement.follow_btn)
