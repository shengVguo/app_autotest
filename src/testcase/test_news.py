# -*- coding: utf-8 -*-
"""
@File: test_comment.py
@Desc: 跟帖模块测试用例
"""


import allure
import pytest

from page.news_page import NewsPage
from page.home_page import HomePage
from common.element import HomeElement, NewsElement


@pytest.fixture()
def open_graphic_news_page(launcher):
    """从首页进入图文新闻页"""
    home_page = HomePage(launcher)
    home_page.skip_ad()
    return home_page.go_to_news_page()


class TestNews:

    @allure.severity("critical")
    def test_graphic_news(self, open_graphic_news_page):
        """
        1、进入图文新闻页
        2、查看新闻详情页元素
        """
        news_page = open_graphic_news_page
        assert news_page.is_element_exists(NewsElement.news_title)

    @allure.severity("critical")
    def test_switch_comment_and_content(self, open_graphic_news_page):
        """
        1、进入图文新闻页
        2、点击底部跟帖icon切换到跟帖模块,展示跟帖大logo
        3、点击底部正文icon切换到正文模块,展示新闻标题
        """
        news_page = open_graphic_news_page
        news_page.switch_to_comment()
        assert news_page.is_element_exists(NewsElement.comment_logo)
        news_page.switch_to_news_content()
        assert news_page.is_element_exists(NewsElement.news_title)
