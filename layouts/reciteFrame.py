from qfluentwidgets import Dialog

from utils.uitools import FrameWrapper
from .Ui_recite import Ui_Frame 
from extern import webDict
from utils.audio import AudioPlayer
import re
import settings

import re

def getMaskedText(text, mask_char='_'):
    # 要保留的词性词（支持多种词性）
    return mask_char* len(text)  # 简单的实现，直接将文本全部替换为下划线
    # pos_tags = ['n.', 'v.', 'adj.', 'adv.', 'pron.', 'prep.', 'conj.', 'interj.', 'a.', 'vt.', 'vi.']
 
    # # 占位替换表
    # placeholder_map = {}
    
    # # 替换词性词为唯一占位符
    # def replace_pos(match):
    #     tag = match.group(0)
    #     placeholder = f"__POS_{len(placeholder_map)}__"
    #     placeholder_map[placeholder] = tag
    #     return placeholder
    
    # pattern = r'\b(?:' + '|'.join(re.escape(tag) for tag in pos_tags) + r')\b'
    # text_with_placeholders = re.sub(pattern, replace_pos, text)

    # # 替换非占位符中的字母为 mask_char
    # masked = ''
    # i = 0
    # while i < len(text_with_placeholders):
    #     # 检查是否是占位符开头
    #     if text_with_placeholders.startswith('__POS_', i):
    #         end = text_with_placeholders.find('__', i + 6)
    #         if end != -1:
    #             end += 2  # 包含后面的两个 _
    #             placeholder = text_with_placeholders[i:end]
    #             masked += placeholder
    #             i = end
    #         else:
    #             # fallback 防止死循环
    #             masked += text_with_placeholders[i]
    #             i += 1
    #     else:
    #         ch = text_with_placeholders[i]
    #         if ch.isalpha():
    #             masked += mask_char
    #         else:
    #             masked += ch
    #         i += 1

    # # 替换回原始词性词
    # for placeholder, tag in placeholder_map.items():
    #     masked = masked.replace(placeholder, tag)

    # return masked



class ReciteFrame(FrameWrapper):
    """ 背单词界面初始化 """
    def __init__(self, parent=None, unique_name=None):
        self.root = parent
        self.wordList = settings.get_todays_word_list()
        self.currentWordIndex = 0
        self.currentWord = self.wordList[self.currentWordIndex].word
        self.currentTranslation = self.wordList[self.currentWordIndex].translation
        self.pronounceUK = self.wordList[self.currentWordIndex].phonetic_uk
        self.pronounceUS = self.wordList[self.currentWordIndex].phonetic_us
        self.player = AudioPlayer()
        super().__init__(Ui_Frame(), parent=parent, unique_name=unique_name)
        self.frame.ok.hide()
        self.frame.notok.hide()
        self.frame.next.hide()
        self.frame.pronounceLabel1.setText("[英]"+self.pronounceUK)
        self.frame.pronounceLabel2.setText("[美]"+self.pronounceUS)
        self.frame.wordLabel.setText(self.currentWord)
        self.frame.progressBar.setProperty('value', 0)
        self.frame.explanationLabel.setText(getMaskedText(self.currentTranslation))
        if settings.get_favourite_status(self.wordList[self.currentWordIndex].id):
            self.frame.favouriteButton.blockSignals(True)  # 阻止信号触发
            self.frame.favouriteButton.setChecked(True)
            self.frame.favouriteButton.blockSignals(False)
        else:
            self.frame.favouriteButton.blockSignals(True)
            self.frame.favouriteButton.setChecked(False)
            self.frame.favouriteButton.blockSignals(False)

    """不同按钮"""
    def switch_knownButton(self):
        self.frame.knownButton.hide()
        self.frame.unknownButton.hide()
        self.frame.ok.show()
        self.frame.notok.show()
        self.frame.explanationLabel.setText(self.currentTranslation)
    def switch_unknownButton(self):
        self.addToFavourite(True)
        self.frame.knownButton.hide()
        self.frame.unknownButton.hide()
        self.frame.next.show()
        self.frame.explanationLabel.setText(self.currentTranslation)
    def switch_ok(self):
        self.frame.ok.hide()
        self.frame.notok.hide()
        self.frame.next.show()
    def switch_notok(self):
        self.addToFavourite(True)
        self.frame.ok.hide()
        self.frame.notok.hide()
        self.frame.next.show()
    def switch_next(self):
        self.frame.ok.hide()
        self.frame.notok.hide()
        self.frame.next.hide()
        self.frame.knownButton.show()
        self.frame.unknownButton.show()
        settings.set_learned(self.wordList[self.currentWordIndex].id)
        self.currentWordIndex += 1
        self.frame.progressBar.setProperty('value', self.currentWordIndex / len(self.wordList) * 100)
        self.logEvent(f'当前单词索引: {self.currentWordIndex}, 总单词数: {len(self.wordList)}')
        if self.currentWordIndex >= len(self.wordList):
            self.logEvent('已完成今日单词的背诵')
            self.frame.wordLabel.setText('😀')
            self.frame.explanationLabel.setText('今日单词已全部背诵完成！')
            self.frame.pronounceLabel1.setText('')
            self.frame.pronounceLabel2.setText('')
            self.frame.favouriteButton.hide()
            self.frame.knownButton.hide()
            self.frame.unknownButton.hide()
            self.frame.ok.hide()
            self.frame.notok.hide()
            self.frame.next.hide()
            self.frame.pronBtn1.hide()
            self.frame.pronBtn2.hide()
        else:
            self.currentWord = self.wordList[self.currentWordIndex].word
            self.currentTranslation = self.wordList[self.currentWordIndex].translation
            self.pronounceUK = self.wordList[self.currentWordIndex].phonetic_uk
            self.pronounceUS = self.wordList[self.currentWordIndex].phonetic_us
            self.frame.pronounceLabel1.setText("[英]"+self.pronounceUK)
            self.frame.pronounceLabel2.setText("[美]"+self.pronounceUS)
            self.frame.wordLabel.setText(self.currentWord)
            self.frame.explanationLabel.setText(getMaskedText(self.currentTranslation))
            if settings.get_favourite_status(self.wordList[self.currentWordIndex].id):
                self.frame.favouriteButton.blockSignals(True)
                self.frame.favouriteButton.setChecked(True)
                self.frame.favouriteButton.blockSignals(False)
            else:
                self.frame.favouriteButton.blockSignals(True)
                self.frame.favouriteButton.setChecked(False)
                self.frame.favouriteButton.blockSignals(False)
    """连接信号和槽函数"""
    def setupConnections(self):
        self.frame.favouriteButton.clicked.connect(lambda: self.addToFavourite())
        self.frame.knownButton.clicked.connect(lambda: self.switch_knownButton())
        self.frame.unknownButton.clicked.connect(lambda: self.switch_unknownButton())
        self.frame.ok.clicked.connect(lambda: self.switch_ok())
        self.frame.notok.clicked.connect(lambda: self.switch_notok())
        self.frame.next.clicked.connect(lambda: self.switch_next())
        self.frame.pronBtn1.clicked.connect(lambda: self.pronounce(1))  # 英式发音按钮
        self.frame.pronBtn2.clicked.connect(lambda: self.pronounce(0))  # 美式发音按钮

    
    def logEvent(self, text):
        print("[log] " + text)
    
    def addToFavourite(self, force:bool=False):
        word = self.wordList[self.currentWordIndex]
        if force:
            self.frame.favouriteButton.blockSignals(True)  # 阻止信号触发
            self.frame.favouriteButton.setChecked(True)
            self.frame.favouriteButton.blockSignals(False)
        if not self.frame.favouriteButton.isChecked():
            self.logEvent('从收藏夹中删除'+word.word)
            settings.remove_favourite(word.id)
        else:
            self.logEvent('添加到收藏夹'+word.word)
            settings.add_favourite(word.id)

    def pronounce(self, type:int):
        """
        发音按钮点击事件
        type: 0 - 英式发音, 1 - 美式发音
        """
        # if type == 0:
        #     self.logEvent('英式发音按钮被点击')
        # elif type == 1:
        #     self.logEvent('美式发音按钮被点击')
        
        file = webDict.query_spelling(self.currentWord, type)
        if file:
            self.player.play(file)
        else:
            self.logEvent('发音查询失败')
        
    def updateWindow(self):
        pass