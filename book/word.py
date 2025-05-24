"""
处理单词相关的操作
"""
import pandas as pd
import os

def get_root_dir():
    return os.path.dirname(os.path.abspath(__file__))

book = pd.read_csv((get_root_dir()+'\\DictionaryData\\book.csv'), sep=">")
word = pd.read_csv((get_root_dir()+'\\DictionaryData\\word.csv'), sep=">")
relation_book_word = pd.read_csv((get_root_dir()+'\\DictionaryData\\relation_book_word.csv'), sep=">")
word_translation = pd.read_csv((get_root_dir()+'\\DictionaryData\\word_translation.csv'))
#print(word)
print(word_translation)
print(get_root_dir())
class Word:
    def __init__(self, id, word, phonetic_uk, phonetic_us,difficulty,translation):
        self.id = id
        self.word = word
        self.phonetic_uk = phonetic_uk
        self.phonetic_us = phonetic_us
        self.difficulty = difficulty
        self.translation = translation
        self.relation_book_word_id_list = []
        self.book_list = []
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