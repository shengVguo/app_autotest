# -*- coding: utf-8 -*-
"""
@File: base.py
@Desc: 封装BasePage类，封装uiautomator2基础方法
"""


import sys
import time
import logging
import uiautomator2 as u2
from uiautomator2.exceptions import UiObjectNotFoundError, XPathElementNotFoundError
from uiautomator2.xpath import XPathSelector


from utils.get_path import get_root_dir


root_path = get_root_dir()


class BasePage:
    def __init__(self, device: u2.Device = None, wait=5):
        if device is not None:
            self.d = device
        else:
            self.d = u2.connect()
        self.d.implicitly_wait(wait)

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

    # @auto_screenshot
    def find_element(self, loc, wait_time=5):
        """
        寻找元素
        :param loc: 定位方式
        :param wait_time: 等待时间
        :return: 返回元素对象或元素对象列表第一个
        """
        try:
            locator = self._get_locator(loc)
            if "xpath" in locator:
                element = self.d.xpath(locator["xpath"])
                if element.wait(timeout=wait_time):
                    return element
                else:
                    raise XPathElementNotFoundError
            else:
                element = self.d(**locator)
                element.must_wait(
                    timeout=wait_time
                )  # 若找不到元素，则会抛出UiObjectNotFoundError
                if len(element) > 1:
                    return element[0]
                return element
        except (XPathElementNotFoundError, UiObjectNotFoundError) as e:
            logging.error("{}元素定位失败".format(loc))
            raise e
        except Exception as e:
            logging.error("{}元素定位失败".format(loc))
            raise e

    def find_elements(self, loc, wait_time=5):
        """
        寻找元素
        :param loc: 定位方式
        :param wait_time: 等待时间
        :return: 返回元素对象列表
        """
        try:
            locator = self._get_locator(loc)
            if "xpath" in locator:
                elements = self.d.xpath(loc[0][1])
                if elements.wait(timeout=wait_time):
                    return elements.all()
                else:
                    raise XPathElementNotFoundError
            else:
                elements = self.d(**locator)
                elements.must_wait(
                    timeout=wait_time
                )  # 若找不到元素，则会抛出UiObjectNotFoundError
                return elements
        except (XPathElementNotFoundError, UiObjectNotFoundError) as e:
            logging.error("{}元素定位失败".format(loc))
            raise e
        except Exception as e:
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

    def click_positon(self, x, y):
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

    def swipe_until_element_found(self, loc, wait_after_found=0.0, **kwargs):
        """
        判断UI元素是否存在, 不存在则持续向上滑动到底部，直到UI元素在页面内出现
        :param loc: 元素对象
        :param wait_after_found: 找到元素后等待时间
        :return:
        """
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
                logging.info(f"元素{loc}找不到，继续滑动……")
                # 获取滑动前页面下半部分的所有元素
                page_content = self._get_half_page_content()
                self.d.swipe_ext("up")
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

    def swipe_for_click(self, loc, wait_after_click=0.0, **kwargs):
        """
        判断UI元素是否存在, 不存在则持续向上滑动到底部，直到UI元素在页面内出现，再进行点击
        :param loc: 元素对象
        :param wait_after_click: 点击后等待时间
        :return:
        """
        element = self.swipe_until_element_found(loc, **kwargs)
        element.click()
        if wait_after_click:
            print("元素找到并点击，sleep {} s".format(wait_after_click))
        time.sleep(wait_after_click)

    def swipe(self, direction: str, distance: int = 6, begin_location=0.2, **kwargs):
        """
        滑动屏幕
        :param direction: 滑动方向：left/right/up/down
        :param distance: 滑动的距离
        :param begin_location: 滑动初始位置
        """
        if (begin_location + 0.1 * distance) > 1:
            logging.error("移动距离超过屏幕最大尺寸")
            raise Exception("移动距离超过屏幕最大尺寸")
        x, y = self.get_screen_size()
        if direction == "left":
            x1 = int(x * (1 - begin_location))
            y1 = int(y * 0.5)
            x2 = int(x * (1 - begin_location - 0.1 * distance))
            self.d.swipe(x1, y1, x2, y1, **kwargs)
            logging.info("向左滑动(%s,%s)->(%s,%s)" % (x1, y1, x2, y1))
        elif direction == "right":
            x1 = int(x * (1 - begin_location - 0.1 * distance))
            y1 = int(y * 0.5)
            x2 = int(x * (1 - begin_location))
            self.d.swipe(x1, y1, x2, y1, **kwargs)
            logging.info("向右滑动(%s,%s)->(%s,%s)" % (x1, y1, x2, y1))
        elif direction == "up":
            x1 = int(x * 0.5)
            y1 = int(y * (1 - begin_location))
            y2 = int(y * (1 - begin_location - 0.1 * distance))
            self.d.swipe(x1, y1, x1, y2, **kwargs)
            logging.info("向上滑动(%s,%s)->(%s,%s)" % (x1, y1, x1, y2))
        elif direction == "down":
            x1 = int(x * 0.5)
            y1 = int(y * (1 - begin_location - 0.1 * distance))
            y2 = int(y * (1 - begin_location))
            self.d.swipe(x1, y1, x1, y2, **kwargs)
            logging.info("向下滑动(%s,%s)->(%s,%s)" % (x1, y1, x1, y2))
        else:
            logging.error("direction must in left/right/up/down!")
            raise Exception("direction must in left/right/up/down!")

    def get_screenshot(self, size: tuple = None):
        """
        获取截图
        :param size: 截图区域大小元组(x,y,width,height)
        :return: 截图路径
        """
        # 获取调用该方法的调用方方法名
        name = sys._getframe(1).f_code.co_name
        times = time.strftime("%Y%m%d-%H%M")
        path = root_path + "/screenshots/" + name + "-" + times + ".png"
        img = self.d.screenshot()
        img.crop(size).save(path)
        logging.info("保存截图：{}".format(path))
        return path


    def find_image_element(self, loc, **kwargs):
        """
        在截图中寻找目标图片元素
        :param loc: 目标图片定位方式
        :param kwargs:
        :return: 对比通过则返回中心坐标
        """
        target = root_path + "/" + loc[0][1]
        logging.debug("image定位元素{}".format(loc))
        element = ImageElement(device=self.d, target=target, **kwargs)
        if element.exsits():
            return element
        else:
            logging.error("{}image元素定位失败".format(loc))
            raise ImageElementNotFoundError

    def check_image_element_exists(self, loc, **kwargs):
        """
        检测图片元素是否存在
        :param loc: 目标图片定位方式
        :param kwargs:
        """
        try:
            self.find_image_element(loc, **kwargs)
            logging.info(f"存在元素{loc}")
            return True
        except ImageElementNotFoundError:
            logging.info(f"不存在元素{loc}")
            return False

    def click_image_element(self, loc, **kwargs):
        """
        点击图片元素
        :param loc: 目标图片定位方式
        :param kwargs:
        """
        try:
            logging.info("点击元素{}".format(loc))
            element = self.find_image_element(loc, **kwargs)
            element.click()
        except Exception as e:
            raise e

    def get_element_bounds(self, loc, wait_time=5):
        """
        获取元素的坐标
        :param element: 元素对象
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
        :param element: 元素对象
        :return: 元素中心坐标元组
        """
        logging.info("获取元素中心坐标{}".format(loc))
        return self.find_element(loc, wait_time=wait_time).center()

    def check_element_exist(self, loc, wait_time=5) -> bool:
        """
        检查元素是否存在
        :param loc: 定位方式
        :param wait_time: 等待时间
        :return: True/False
        """
        try:
            self.find_element(loc, wait_time=wait_time).wait()
        except Exception as e:
            logging.info(f"不存在元素{loc}")
            return False
        else:
            logging.info(f"存在元素{loc}")
            return True

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
