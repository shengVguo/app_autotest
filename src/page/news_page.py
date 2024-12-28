# -*- coding: utf-8 -*-
"""
@File: news_page.py
@Desc: 新闻内容页page
"""

import logging
from common.app import App
from common.element import NewsElement


class NewsPage(App):

    def get_page_title(self):
        """获取内容页面新闻标题"""
        return self.get_text(NewsElement.news_title)

    def switch_to_comment(self):
        """点击底部跟帖icon，切换到跟贴区"""
        self.click_element(NewsElement.comment_icon)

    def switch_to_news_content(self):
        """点击底部正文icon，切换到新闻正文区"""
        self.click_element(NewsElement.news_content_icon)

    def follow_author(self):
        """点击关注作者"""
        self.click_element(NewsElement.follow_btn)

    def cancel_follow_author(self):
        """点击取消关注"""
        self.click_element(NewsElement.cancel_follow_btn)
