

from common.app import App
from common.element import CommentElement
class CommentPage(App):

    def edit_and_send_comment_content(self, content):
        '''点击写跟帖，输入跟帖内容，发送'''
        # self.click_element(CommentElement.comment_edit_trigger)
        self.input(CommentElement.comment_edit, content)
        self.click_element(CommentElement.send_comment_btn)

    def is_send_btn_enable(self):
        '''发送按钮是否可用'''
        return self.get_element_info(CommentElement.send_comment_btn, key='enabled')

    def is_exist_comment_content(self, content):
        '''检查指定跟帖内容是否存在'''
        return self.check_element_exist(CommentElement.comment_content_text(content))