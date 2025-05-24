"""
处理书籍相关操作
"""
import pandas as pd
import os

def get_root_dir():
    return os.path.dirname(os.path.abspath(__file__))

book = pd.read_csv((get_root_dir()+'\\DictionaryData\\book.csv'), sep=">")
word = pd.read_csv((get_root_dir()+'\\DictionaryData\\word.csv'), sep=">")
relation_book_word = pd.read_csv((get_root_dir()+'\\DictionaryData\\relation_book_word.csv'), sep=">")
word_translation = pd.read_csv((get_root_dir()+'\\DictionaryData\\word_translation.csv'))

class Book:
    def __init__(self, id, title, word_count):
        self.id = id
        self.title = title
        self.word_count = word_count
        self.relation_book_word_id_list = []
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