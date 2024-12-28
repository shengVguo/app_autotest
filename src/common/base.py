# -*- coding: utf-8 -*-
"""
@File: base.py
@Desc: 封装BasePage类，封装uiautomator2基础方法
"""


import time
import logging
import uiautomator2 as u2
from uiautomator2.exceptions import UiObjectNotFoundError, XPathElementNotFoundError

from utils.get_path import get_root_dir


root_path = get_root_dir()


class BasePage:
    def __init__(self, device: u2.Device = None):
        if device is not None:
            self.d = device
        else:
            self.d = u2.connect()

    def _get_locator(self, loc: tuple):
        """
        处理定位方式
        :param loc: 定位方式
        :return:
        """
        if len(loc) == 2:
            logging.info("定位元素{}".format(loc))
            return {loc[0]: loc[1]}
        else:
            raise ValueError("定位方式错误!")

    def _find_element_common(self, loc, wait_time=5, is_single=True):
        """
        通用的元素查找私有方法，可用于查找单个元素或多个元素
        :param loc: 元素定位信息，格式为 (定位类型, 定位表达式)
        :param wait_time: 等待元素出现的超时时间，默认5秒
        :param is_single: 是否查找单个元素，True表示查找单个元素，False表示查找多个元素
        :return: 找到的元素对象或元素对象列表
        :raises XPathElementNotFoundError: 如果使用xpath定位且元素未找到时抛出此异常
        :raises UiObjectNotFoundError: 如果使用其他定位方式且元素未找到时抛出此异常
        :raises Exception: 其他未知异常
        """
        locator = self._get_locator(loc)
        if "xpath" in locator:
            elements = self.d.xpath(locator["xpath"])
            if elements.wait(timeout=wait_time):
                return elements if is_single else elements.all()
            else:
                raise XPathElementNotFoundError
        else:
            elements = self.d(**locator)
            elements.must_wait(timeout=wait_time)
            return elements[0] if is_single and len(elements) > 0 else elements

    # @auto_screenshot
    def find_element(self, loc, wait_time=5):
        """
        寻找单个元素
        :param loc: 定位方式，格式为 (定位类型, 定位表达式)
        :param wait_time: 等待元素出现的超时时间，默认5秒
        :return: 返回找到的元素对象
        """
        try:
            return self._find_element_common(loc, wait_time=wait_time, is_single=True)
        except (XPathElementNotFoundError, UiObjectNotFoundError, Exception) as e:
            logging.error("{}元素定位失败".format(loc))
            raise e

    def find_elements(self, loc, wait_time=5):
        """
        寻找多个元素
        :param loc: 定位方式，格式为 (定位类型, 定位表达式)
        :param wait_time: 等待元素出现的超时时间，默认5秒
        :return: 返回找到的元素对象列表
        """
        try:
            return self._find_element_common(loc, wait_time=wait_time, is_single=False)
        except (XPathElementNotFoundError, UiObjectNotFoundError, Exception) as e:
            logging.error("{}元素定位失败".format(loc))
            raise e

    def get_element_info(self, loc, **kwargs):
        """
        获取元素信息
        :param loc: 定位方式
        :param key: 信息键值
        :return: 返回元素信息
        """
        try:
            info = self.find_element(loc, wait_time=kwargs.get("wait_time", 5)).info
        except Exception as e:
            logging.error("获取元素信息失败{}".format(e))
            raise e
        key = kwargs.get("key")
        return info.get(key) if key is not None else info

    def get_text(self, loc, **kwargs):
        """
        获取元素的文本
        :param loc: 定位方式
        :param kwargs:
        :return: 返回元素文本
        """
        try:
            text = self.find_element(loc, **kwargs).get_text()
            logging.info(f"获取元素{loc}文本：{text}")
        except Exception as e:
            logging.error("获取元素文本失败{}".format(e))
            raise e
        return text

    def _get_element_click_position(self, loc, offset: tuple = (0.5, 0.5), **kwargs):
        """
        获取元素点击位置
        :param element: 元素对象
        :param offset: 偏移量
        """
        try:
            element = self.find_element(loc, **kwargs)
            if isinstance(element, u2.UiObject):
                return element.center(offset)
            else:
                return element.offset(*offset)
        except Exception as e:
            logging.error("获取元素点击位置失败{}".format(e))
            raise e

    def click_element(self, loc, **kwargs):
        """
        点击元素
        :param loc: 定位方式
        :param kwargs:
        :return:
        """
        logging.info("点击元素{}".format(loc))
        try:
            click_position = self._get_element_click_position(loc, **kwargs)
            self.d.click(*click_position)
        except Exception as e:
            logging.error("点击元素失败，{}".format(loc))
            raise e

    def click_position(self, x, y):
        """
        点击坐标或者元素坐标
        :param x: x坐标
        :param y: y坐标
        """
        logging.info("点击坐标{}".format((x, y)))
        self.d.click(x, y)

    def long_click(self, loc, **kwargs):
        """
        长按元素或者坐标
        :param loc: 定位方式
        :param position: 坐标，和定位方式二选一，若传递的positon,则直接点击position
        :param kwargs:
        """
        duration = kwargs.pop("duration", 5.0)
        logging.info("长按元素{}".format(loc))
        try:
            click_position = self._get_element_click_position(loc, **kwargs)
            self.d.long_click(*click_position, duration)
        except Exception as e:
            logging.error("长按元素失败，{}".format(loc))
            raise e

    def input(self, loc, word):
        """
        输入
        :param loc: 定位方式
        :param word: 输入内容
        """
        logging.info("元素{}，输入:{}".format(loc, word))
        self.find_element(loc).set_text(word)

    def back(self, num=1):
        """
        系统back返回操作
        :param num: 返回的层数
        """
        for i in range(num):
            logging.info("点击返回")
            self.d.press("back")

    def get_screen_size(self) -> tuple:
        """
        获取屏幕分辨率
        :return: 屏幕分辨率元组(width,height)
        """
        return self.d.window_size()

    def _get_half_page_content(self):
        """
        获取页面下半部分内容
        :return: 页面内容
        """
        return self.d.dump_hierarchy()[(len(self.d.dump_hierarchy()) // 2) :]

    def _is_page_content_changed(self, page_content):
        """
        判断页面内容是否发生变化
        :param page_content: 页面内容
        :return: True or False
        """
        return self._get_half_page_content() != page_content

    def swipe_until_element_found(
        self, loc, direction="up", max_timeout=30, wait_after_found=0.0, **kwargs
    ):
        """
        判断UI元素是否存在，若不存在则持续向上滑动页面查找，直到UI元素在页面内出现或者达到最长超时时间

        :param loc: 元素定位信息，格式为 (定位类型, 定位表达式)
        :param direction: 滑动方向，默认为向上滑动，可选值为 'up'、'down'、'left'、'right'
        :param max_timeout: 最长超时时间，单位为秒，默认30秒，表示从开始查找元素到最终放弃查找的总时长限制，超过此时间未找到元素则抛出异常
        :param wait_after_found: 找到元素后等待时间，单位为秒，默认0.0秒，用于在找到元素后暂停一定时间，可用于等待元素状态稳定等情况
        :param kwargs: 其他可选参数
        :return: 返回找到的元素对象
        :raises AssertionError: 如果在最长超时时间内未找到元素，则抛出此异常，表示元素在该页面找不到
        """
        start_time = time.time()  # 记录开始查找的时间
        found_element = False  # 定义标志变量表示元素是否被找到
        while True:
            try:
                element = self.find_element(loc, wait_time=2)
                found_element = True  # 成功找到元素，设置标志为 True
                if wait_after_found:
                    logging.debug(f"元素找到，sleep {wait_after_found} s")
                time.sleep(wait_after_found)
                return element
            except (UiObjectNotFoundError, XPathElementNotFoundError) as e:
                current_time = time.time()  # 获取当前时间
                if current_time - start_time > max_timeout:  # 判断是否超过最长超时时间
                    logging.error(
                        f"达到最长超时时间 {max_timeout} 秒，仍未找到元素 {loc}，跳出循环"
                    )
                    break
                logging.info(f"元素{loc}找不到，继续滑动……")
                # 获取滑动前页面下半部分的所有元素
                page_content = self._get_half_page_content()
                self.d.swipe_ext(direction)
                time.sleep(0.5)
                # 获取滑动后页面下半部分的所有元素，并与上一次滑动前的页面元素对比，页面元素没有变化时跳出循环
                if not self._is_page_content_changed(page_content):
                    logging.error(f"页面元素没有变化，跳出循环, {e}")
                    break
            except Exception as e:
                logging.error(f"元素定位失败{e}")
                break
        if not found_element:  # 根据标志变量判断元素最终是否被找到
            raise AssertionError(f"元素{loc}在该页面找不到")

    def swipe_for_click(self, loc, **kwargs):
        """
        判断UI元素是否存在, 不存在则持续向上滑动到底部，直到UI元素在页面内出现，再进行点击
        :param loc: 元素对象
        :param kwargs: 参考swipe_until_element_found方法
        :return:
        """
        try:
            element = self.swipe_until_element_found(loc, **kwargs)
            element.click()
        except Exception as e:
            logging.error(f"元素点击失败{e}")
            raise e

    def swipe(self, direction: str, distance: int = 0.6, begin_location=0.2, **kwargs):
        """
        滑动屏幕
        :param direction: 滑动方向：left/right/up/down
        :param distance: 滑动的距离 (0.0, 1.0)
        :param begin_location: 滑动初始位置
        """
        if (begin_location + distance) > 1:
            logging.error("移动距离超过屏幕最大尺寸")
            raise Exception("移动距离超过屏幕最大尺寸")
        x, y = self.get_screen_size()
        if direction == "left":
            x1 = int(x * (1 - begin_location))
            y1 = int(y * 0.5)
            x2 = int(x * (1 - begin_location - distance))
            self.d.swipe(x1, y1, x2, y1, **kwargs)
            logging.info("向左滑动(%s,%s)->(%s,%s)" % (x1, y1, x2, y1))
        elif direction == "right":
            x1 = int(x * (1 - begin_location - distance))
            y1 = int(y * 0.5)
            x2 = int(x * (1 - begin_location))
            self.d.swipe(x1, y1, x2, y1, **kwargs)
            logging.info("向右滑动(%s,%s)->(%s,%s)" % (x1, y1, x2, y1))
        elif direction == "up":
            x1 = int(x * 0.5)
            y1 = int(y * (1 - begin_location))
            y2 = int(y * (1 - begin_location - distance))
            self.d.swipe(x1, y1, x1, y2, **kwargs)
            logging.info("向上滑动(%s,%s)->(%s,%s)" % (x1, y1, x1, y2))
        elif direction == "down":
            x1 = int(x * 0.5)
            y1 = int(y * (1 - begin_location - distance))
            y2 = int(y * (1 - begin_location))
            self.d.swipe(x1, y1, x1, y2, **kwargs)
            logging.info("向下滑动(%s,%s)->(%s,%s)" % (x1, y1, x1, y2))
        else:
            logging.error("direction must in left/right/up/down!")
            raise Exception("direction must in left/right/up/down!")

    def get_element_bounds(self, loc, wait_time=5):
        """
        获取元素的坐标
        :param loc: 元素对象
        :return: 元素坐标元组(left, top, right, bottom)
        """
        logging.info("获取元素坐标{}".format(loc))
        element = self.find_element(loc, wait_time=wait_time)
        if isinstance(element, u2.UiObject):
            return element.bounds()
        elif isinstance(element, u2.xpath.XPathSelector):
            return element.bounds

    def get_element_center(self, loc, wait_time=5):
        """
        获取元素的中心坐标
        :param loc: 元素对象
        :return: 元素中心坐标元组
        """
        logging.info("获取元素中心坐标{}".format(loc))
        return self.find_element(loc, wait_time=wait_time).center()

    def is_element_exists(
        self, loc, use_swipe=False, max_timeout=30, wait_time=5, **kwargs
    ):
        """
        检查元素是否存在，可选择是否通过滑动页面来查找元素进行判断
        :param loc: 元素定位信息，格式为 (定位类型, 定位表达式)
        :param use_swipe: 是否使用滑动查找元素，默认False，表示仅通过常规定位方式判断元素是否存在，若为True，则启用滑动查找功能
        :param max_timeout: 最长超时时间，当use_swipe为True时有效，单位为秒，默认30秒，表示从开始查找元素到最终放弃查找的总时长限制，超过此时间未找到元素则返回False
        :param wait_time: 等待时间，用于常规元素定位时等待元素出现的超时时间，默认5秒
        :param kwargs:
        :return: True表示找到了元素，False表示未找到元素
        """
        if not use_swipe:
            try:
                self.find_element(loc, wait_time=wait_time)
                return True
            except Exception as e:
                logging.info(f"元素{loc}不存在")
                return False
        else:
            try:
                element = self.swipe_until_element_found(
                    loc, max_timeout=max_timeout, **kwargs
                )
                return element is not None
            except AssertionError as ae:
                logging.info(f"通过滑动查找未找到元素 {loc}")
                return False

    def pinch_in(self, loc, **kwargs):
        """
        缩小操作
        :param loc: 定位方式
        """
        if loc:
            self.find_element(loc).pinch_in(**kwargs)
        else:
            self.d().pinch_in(**kwargs)

    def pinch_out(self, loc, **kwargs):
        """
        放大操作
        :param loc: 定位方式
        """
        if loc:
            self.find_element(loc).pinch_out(**kwargs)
        else:
            self.d().pinch_out(**kwargs)
