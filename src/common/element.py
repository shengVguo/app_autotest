# -*- coding: utf-8 -*-
"""
@File: element.py
@Desc: 元素控件类
"""

from utils.by import By


class CommonElement:
    skip_ad = (By.ID, "com.netease.newsreader.activity:id/biz_ad_skip")
    bar_back = (By.ID, "com.netease.newsreader.activity:id/action_bar_back")


class HomeElement(CommonElement):
    home_tab = (
        By.XPATH,
        '//*[@resource-id="com.netease.newsreader.activity:id/biz_navi_title" and @text="首页"]',
    )
    headline_title = (
        By.XPATH,
        '//*[@resource-id="com.netease.newsreader.activity:id/title" and @text="头条"]',
    )

    pull_to_refresh_prompt = (By.ID, "com.netease.newsreader.activity:id/prompt")

    # 通用新闻卡片,通过子元素寻找先辈元素
    _generate_news_card = lambda child_id: (
        By.XPATH,
        f'//*[@resource-id="{child_id}"]/ancestor::*[@resource-id="com.netease.newsreader.activity:id/card_wrapper_container"]',
    )
    news_card_title = (By.ID, "com.netease.newsreader.activity:id/show_style_title")

    # 无封面新闻
    no_cover_news_card = _generate_news_card("com.netease.newsreader.activity:id/title")

    # 单图新闻
    single_image_news_card = _generate_news_card(
        "com.netease.newsreader.activity:id/image"
    )
    single_image = (By.ID, "com.netease.newsreader.activity:id/image")

    # 多图新闻
    multi_image_news_card = _generate_news_card(
        "com.netease.newsreader.activity:id/multi_image"
    )
    multi_image_news_title = (
        By.XPATH,
        '//*[@resource-id="com.netease.newsreader.activity:id/multi_image"',
    )
    multi_image = (By.ID, "com.netease.newsreader.activity:id/multi_image")

    # 视频新闻
    video_news_card = _generate_news_card(
        "com.netease.newsreader.activity:id/video_container"
    )
    video_cover = (By.ID, "com.netease.newsreader.activity:id/video_container")
    video_news_title = (By.ID, "com.netease.newsreader.activity:id/show_style_title")

    hot_comment = (By.ID, "com.netease.newsreader.activity:id/hot_comment_container")


class NewsElement(CommonElement):
    # 顶部导航栏
    top_bar = (By.ID, "com.netease.newsreader.activity:id/action_bar")
    top_bar_comment_num = (
        By.ID,
        "com.netease.newsreader.activity:id/action_bar_comment_num",
    )
    search_btn = (By.ID, "com.netease.newsreader.activity:id/action_bar_search")
    more_btn = (By.ID, "com.netease.newsreader.activity:id/action_bar_more")

    # 新闻标题
    news_title = (By.XPATH, '//*[@resource-id="article"]/android.widget.TextView[1]')

    # 来源作者信息
    author_info = (By.ID, "reader")
    follow_btn = (By.XPATH, '//android.widget.Button[@text="关注"]')
    cancel_follow_btn = (By.XPATH, '//android.widget.Button[@text="已关注"]')

    # 正文部分
    illustration = (By.XPATH, '//android.widget.Image[@text="图片"]')

    # 大图查看页元素
    fullscreen_picture = (By.ID, "com.netease.newsreader.activity:id/picture")
    picture_counter = (By.ID, "com.netease.newsreader.activity:id/counter_fullscreen")
    download_btn = (By.ID, "com.netease.newsreader.activity:id/download_btn")
    close_btn = (
        By.ID,
        "com.netease.newsreader.activity:id/news_top_bar_default_state_left",
    )

    # 底部操作栏
    bottom_bar = (By.ID, "com.netease.newsreader.activity:id/reply_container")
    comment_input = (By.ID, "com.netease.newsreader.activity:id/reply_edit_trigger")
    comment_icon = (By.ID, "com.netease.newsreader.activity:id/reply_comment_icon")
    news_content_icon = (
        By.ID,
        "com.netease.newsreader.activity:id/reply_newspage_icon",
    )
    comment_num = (By.ID, "com.netease.newsreader.activity:id/reply_comment_number")
    support_btn = (
        By.XPATH,
        '//*[@resource-id="com.netease.newsreader.activity:id/attitude_viewandroid.widget.Button[1]"]',
    )
    unsupport_btn = (
        By.XPATH,
        '//*[@resource-id="com.netease.newsreader.activity:id/attitude_view"]/android.widget.Button[2]',
    )

    comment_logo = (
        By.ID,
        "com.netease.newsreader.activity:id/comment_group_image_container",
    )


class CommentElement(CommonElement):
    # 网易跟帖4大字logo
    comment_page_logo = (
        By.ID,
        "com.netease.newsreader.activity:id/comment_group_image_container",
    )
    # 跟帖内容区
    commenter_avator = (By.ID, "com.netease.newsreader.activity:id/item_header_avater")
    commenter_name = (By.ID, "com.netease.newsreader.activity:id/item_header_user_info")
    comment_time_orig = (
        By.ID,
        "com.netease.newsreader.activity:id/item_header_time_orig",
    )
    comment_content = (By.ID, "com.netease.newsreader.activity:id/item_content_content")
    comment_time = (By.ID, "com.netease.newsreader.activity:id/item_footer_time")
    comment_content_text = lambda text: (
        By.XPATH,
        f'//*[@resource-id="com.netease.newsreader.activity:id/item_content_content" and @text="{text}"]',
    )
    # 不支持跟帖
    unsupport_comment_btn = (
        By.ID,
        "com.netease.newsreader.activity:id/lottie_support_view",
    )
    unsupport_comment_num = (
        By.XPATH,
        '//*[@resource-id="com.netease.newsreader.activity:id/item_header_unsupport"]/descendant::*[@resource-id="com.netease.newsreader.activity:id/support_num"]',
    )
    # 支持跟帖
    support_comment_btn = (By.ID, "com.netease.newsreader.activity:id/support_icon")
    support_comment_num = (By.ID, "com.netease.newsreader.activity:id/support_num")
    # 评论操作区
    comment_reply = (By.ID, "com.netease.newsreader.activity:id/item_footer_reply")
    comment_menu = (By.ID, "com.netease.newsreader.activity:id/item_footer_menu")
    # 写跟帖输入框
    comment_edit_trigger = (
        By.ID,
        "com.netease.newsreader.activity:id/reply_edit_trigger",
    )
    comment_edit = (By.ID, "com.netease.newsreader.activity:id/comment_reply_edit")
    send_comment_btn = (By.ID, "com.netease.newsreader.activity:id/comment_reply_send")
