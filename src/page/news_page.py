

from common.app import App
from common.element import NewsElement
class NewsPage(App):

    def get_page_title(self):
        return self.get_text(NewsElement.news_title)




