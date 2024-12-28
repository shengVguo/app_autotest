# -*- coding: utf-8 -*-
"""
@File: home_page.py
@Desc: 首页page
"""

import time
import logging

from common.app import App
from common.element import HomeElement
from page.news_page import NewsPage
from page.comment_page import CommentPage


class HomePage(App):

    def is_element_selected(self, loc):
        """元素是否被选中"""
        return self.get_element_info(loc, key="selected")

    def is_single_image_news_card_present(self):
        """是否存在单图片新闻卡片"""
        return self.is_element_exists(HomeElement.single_image_news_card, use_swipe=True)

    def is_multi_image_news_card_present(self):
        """是否存在多图片封面新闻卡片"""
        return self.is_element_exists(HomeElement.multi_image_news_card, use_swipe=True)

    def is_video_news_card_present(self):
        """是否存在视频封面新闻卡片"""
        return self.is_element_exists(HomeElement.video_news_card, use_swipe=True)

    def go_to_news_page(self, loc=HomeElement.single_image_news_card):
        """
        点击新闻标题进入新闻内容页
        """
        self.swipe_for_click(loc)
        return NewsPage(self.d)

    def go_to_video_page(self, loc=HomeElement.video_news_card):
        """
        点击视频封面进入视频播放页
        """
        self.swipe_for_click(loc)
        return NewsPage(self.d)

    def go_to_comment_page(self, loc=HomeElement.hot_comment):
        """
        点击热评进入评论页
        """
        self.swipe_for_click(loc)
        return CommentPage(self.d)

    def current_page_content(self):
        return self.d.dump_hierarchy()

    def pull_to_refresh(self):
        self.swipe(direction="down")
        self.swipe(direction="down")
