# -*- coding: utf-8 -*-
"""
@File: test_comment.py
@Desc: 跟帖页模块测试用例
"""
import pytest
from page.home_page import HomePage
from page.comment_page import CommentPage
from common.element import CommentElement


@pytest.fixture()
def open_comment_page(launcher):
    home_page = HomePage(launcher)
    home_page.skip_ad()
    return home_page.go_to_comment_page()


class TestComment:

    def test_comment_page(self, open_comment_page):
        """
        1、从首页热评进入跟帖页
        2、检查网易跟帖大logo
        3、检查跟帖人头像、名称、地点
        4、检查跟帖内容
        5、检查跟帖发布时间
        """
        comment_page = open_comment_page
        assert comment_page.check_element_exist(CommentElement.comment_page_logo)
        assert comment_page.check_element_exist(CommentElement.commenter_avator)
        assert comment_page.check_element_exist(CommentElement.commenter_name)
        assert comment_page.check_element_exist(CommentElement.comment_time_orig)
        assert comment_page.check_element_exist(CommentElement.comment_content)
        assert comment_page.check_element_exist(CommentElement.comment_time)
    @pytest.mark.parametrize("comment_content", ["这是我的测试跟帖内容1", "这是我的测试跟帖内容2"])
    def test_send_comment(self, open_comment_page, comment_content):
        """
        1、从首页热评进入跟帖页
        2、点击写跟贴
        3、不输入内容，查看发送按钮是否可点击
        4、编辑跟帖内容，并发送
        5、检查跟帖页是否有刚发送的跟帖内容
        """
        comment_page = open_comment_page
        comment_page.click_element(CommentElement.comment_edit_trigger)
        assert not comment_page.is_send_btn_enable()
        comment_page.edit_and_send_comment_content(comment_content)
        assert comment_page.is_exist_comment_content(comment_content)
