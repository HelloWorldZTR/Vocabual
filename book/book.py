"""
处理书籍相关操作
"""


class Book:
    def __init__(self, title, cover, word_count, word_list_db_table):
        self.title = title
        self.cover = cover
        self.word_count = word_count
        self.word_list_db_table = word_list_db_table
        self.word_list = []
    def load_from_db(self):
        """
        从数据库加载单词列表
        """
        pass
    def get_today_word(self):
        """
        获取今天的单词
        """
        pass