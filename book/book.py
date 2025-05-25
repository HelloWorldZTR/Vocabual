"""
处理书籍相关操作
"""
import pandas as pd
import os


class Book:
    def __init__(self, id, title, word_count):
        self.id = id
        self.title = title
        self.word_count = word_count
        self.relation_book_word_id_list = []
        self.word_list = []