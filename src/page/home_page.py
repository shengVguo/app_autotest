


import time
import logging

from common.app import App
from common.element import HomeElement
from page.news_page import NewsPage
from page.comment_page import CommentPage


class HomePage(App):

    def is_element_selected(self, loc):
        '''元素是否被选中'''
        return self.get_element_info(loc, key='selected')
    
    def is_exist_single_image_news_card(self):
        '''是否存在单图片新闻卡片'''
        news_card = self.swipe_until_element_found(HomeElement.single_image_news_card)
        return news_card is not None

    def is_exist_multi_image_news_card(self):
        '''是否存在多图片封面新闻卡片'''
        news_card = self.swipe_until_element_found(HomeElement.multi_image_news_card)
        return news_card is not None

    def is_exist_video_news_card(self):
        '''是否存在视频封面新闻卡片'''
        news_card = self.swipe_until_element_found(HomeElement.video_news_card)
        return news_card is not None

    def get_news_card_title(self, loc):
        news_card = self.swipe_until_element_found(loc)
        return news_card.get_text()

    def go_to_news_page(self, loc=HomeElement.single_image_news_card):
        '''
        点击新闻标题进入新闻内容页
        '''
        self.swipe_for_click(loc)
        return NewsPage(self.d)

    def go_to_video_page(self, loc=HomeElement.video_news_card):
        '''
        点击视频封面进入视频播放页
        '''
        self.swipe_for_click(loc)
        return NewsPage(self.d)

    def go_to_comment_page(self, loc=HomeElement.hot_comment):
        '''
        点击热评进入评论页
        '''
        self.swipe_for_click(loc)
        return CommentPage(self.d)

    def current_page_content(self):
        return self.d.dump_hierarchy()

    def pull_to_refresh(self):
        self.swipe(direction='down')
        self.swipe(direction='down')
