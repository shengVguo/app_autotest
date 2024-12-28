# -*- coding: utf-8 -*-
"""
@File: app.py
@Desc: 待测app启动、初始化相关方法
"""

import time
import logging

from common.base import BasePage
from common.element import CommonElement, HomeElement


APP_PACKAGE = "com.netease.newsreader.activity"


class App(BasePage):
    def start(self):
        """启动App"""
        if not self.d:
            super().__init__()
        self.d.app_start(APP_PACKAGE, stop=True)
        return self.d

    def restart(self):
        """重启App"""
        self.stop()
        self.start()

    def clear(self):
        """清除app缓存"""
        self.d.app_clear(APP_PACKAGE)

    def stop(self):
        """关闭App"""
        self.d.app_stop(APP_PACKAGE)

    def skip_ad(self):
        """跳过开屏广告"""
        if not self.check_element_exist(HomeElement.home_tab):
            if self.check_element_exist(CommonElement.skip_ad):
                self.click_element(CommonElement.skip_ad)
                time.sleep(2)

    def login(self):
        """登录"""
        pass

    def logout(self):
        """退出登录"""
        pass


if __name__ == "__main__":
    app = App("127.0.0.1:7555")
    app.start()
    app.click_element(CommonElement.skip_ad)
    titles = app.find_elements(CommonElement.title)
    title1 = titles[0]
    titls2 = titles[1]
    print(title1.get_text())
    print(titls2.get_text())
