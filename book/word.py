"""
处理单词相关的操作
"""
import pandas as pd
import os


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