from qfluentwidgets import Dialog
from utils.uitools import FrameWrapper
from .Ui_review import Ui_Frame 
from extern import webDict
from PyQt5.QtCore import QTimer
import settings
import random
import bookdata

class ReviewFrame(FrameWrapper):
    """ 背单词界面初始化 """
    def __init__(self, parent=None, unique_name=None):
        self.root = parent
        self.wordList = settings.get_favourite_list()
        if len(self.wordList) == 0:
            self.logEvent('没有单词可供背诵')
            Dialog.warning(self.root, "没有单词可供背诵", "请先添加单词到收藏夹")
            return
        random.shuffle(self.wordList)  # 随机打乱单词列表
        self.otherWordList = list(bookdata.words.values())
        #print(type(self.otherWordList))
        self.currentWordIndex = 0
        self.currentWord = self.wordList[self.currentWordIndex].word
        self.currentTranslation = self.wordList[self.currentWordIndex].translation
        self.stage=random.randint(0, 1)
        self.answer=random.randint(1,4)
        self.buttons = [None, self.frame.A, self.frame.B, self.frame.C, self.frame.D]
        super().__init__(Ui_Frame(), parent=parent, unique_name=unique_name)
        if self.stage == 0:
            self.frame.wordLabel_2.setText(self.currentWord)
            for i in range(1, 5):
                if i == self.answer:
                    self.buttons[i].setText(self.currentTranslation)
                else:
                    self.buttons[i].setText((random.choice(self.otherWordList)).translation)
        else:
            self.frame.wordLabel_2.setText(self.currentTranslation)
            for i in range(1, 5):
                if i == self.answer:
                    self.buttons[i].setText(self.currentWord)
                else:
                    self.buttons[i].setText((random.choice(self.otherWordList)).word)
    """下一个单词"""
    def nextWord(self):
        self.resetButton()
        self.currentWordIndex += 1
        if self.currentWordIndex >= len(self.wordList):
            self.logEvent('已完成')
            self.frame.wordLabel_2.setText('😀')
        else:
            self.currentWord = self.wordList[self.currentWordIndex].word
            self.currentTranslation = self.wordList[self.currentWordIndex].translation
            self.stage=random.randint(0, 1)
            self.answer=random.randint(1,4)
            if self.stage == 0:
                self.frame.wordLabel_2.setText(self.currentWord)
                for i in range(1, 5):
                    if i == self.answer:
                        self.buttons[i].setText(self.currentTranslation)
                    else:
                        self.buttons[i].setText((random.choice(self.otherWordList)).translation)
            else:
                self.frame.wordLabel_2.setText(self.currentTranslation)
                for i in range(1, 5):
                    if i == self.answer:
                        self.buttons[i].setText(self.currentWord)
                    else:
                        self.buttons[i].setText((random.choice(self.otherWordList)).word)
    """还原按钮"""
    def resetButton(self):
        """还原按钮颜色"""
        self.frame.A.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.frame.B.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.frame.C.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.frame.D.setStyleSheet("background-color: rgb(255, 255, 255);")
    """不同按钮"""
    def A(self):
        if self.answer == 1:
            self.frame.A.setStyleSheet("background-color: rgb(0, 255, 0);")
        elif self.answer == 2:
            self.frame.A.setStyleSheet("background-color: rgb(255, 0, 0);")
            self.frame.B.setStyleSheet("background-color: rgb(0, 255, 0);")
        elif self.answer == 3:
            self.frame.A.setStyleSheet("background-color: rgb(255, 0, 0);")
            self.frame.C.setStyleSheet("background-color: rgb(0, 255, 0);")
        elif self.answer == 4:
            self.frame.A.setStyleSheet("background-color: rgb(255, 0, 0);")
            self.frame.D.setStyleSheet("background-color: rgb(0, 255, 0);")
        #QTimer.singleShot(5000)
        QTimer.singleShot(5000, self.nextWord)
        
    def B(self):
        if self.answer == 1:
            self.frame.B.setStyleSheet("background-color: rgb(0, 255, 0);")
        elif self.answer == 2:
            self.frame.B.setStyleSheet("background-color: rgb(255, 0, 0);")
            self.frame.A.setStyleSheet("background-color: rgb(0, 255, 0);")
        elif self.answer == 3:
            self.frame.B.setStyleSheet("background-color: rgb(255, 0, 0);")
            self.frame.D.setStyleSheet("background-color: rgb(0, 255, 0);")
        elif self.answer == 4:
            self.frame.B.setStyleSheet("background-color: rgb(255, 0, 0);")
            self.frame.C.setStyleSheet("background-color: rgb(0, 255, 0);")
        #QTimer.singleShot(5000)
        QTimer.singleShot(5000, self.nextWord)
    def C(self):
        if self.answer == 1:
            self.frame.C.setStyleSheet("background-color: rgb(0, 255, 0);")
        elif self.answer == 2:
            self.frame.C.setStyleSheet("background-color: rgb(255, 0, 0);")
            self.frame.D.setStyleSheet("background-color: rgb(0, 255, 0);")
        elif self.answer == 3:
            self.frame.C.setStyleSheet("background-color: rgb(255, 0, 0);")
            self.frame.A.setStyleSheet("background-color: rgb(0, 255, 0);")
        elif self.answer == 4:
            self.frame.C.setStyleSheet("background-color: rgb(255, 0, 0);")
            self.frame.B.setStyleSheet("background-color: rgb(0, 255, 0);")
        #QTimer.singleShot(5000)
        QTimer.singleShot(5000, self.nextWord)
    def D(self):
        if self.answer == 1:
            self.frame.D.setStyleSheet("background-color: rgb(0, 255, 0);")
        elif self.answer == 2:
            self.frame.D.setStyleSheet("background-color: rgb(255, 0, 0);")
            self.frame.C.setStyleSheet("background-color: rgb(0, 255, 0);")
        elif self.answer == 3:
            self.frame.D.setStyleSheet("background-color: rgb(255, 0, 0);")
            self.frame.B.setStyleSheet("background-color: rgb(0, 255, 0);")
        elif self.answer == 4:
            self.frame.D.setStyleSheet("background-color: rgb(255, 0, 0);")
            self.frame.A.setStyleSheet("background-color: rgb(0, 255, 0);")
        #QTimer.singleShot(5000)
        QTimer.singleShot(5000, self.nextWord)
        
    """连接信号和槽函数"""
    def setupConnections(self):
        self.frame.A.clicked.connect(self.A)
        self.frame.B.clicked.connect(self.B)
        self.frame.C.clicked.connect(self.C)
        self.frame.D.clicked.connect(self.D)

    def logEvent(self, text):
        print("[log] " + text)
    
    def addToFavourite(self):
        word = self.wordList[self.currentWordIndex]
        self.logEvent('添加到收藏夹'+word.word)
        settings.add_favourite(word.id)
        self.frame.favouriteButton.checked = True

    def pronounce(self, type:int):
        """
        发音按钮点击事件
        type: 0 - 英式发音, 1 - 美式发音
        """
        if type == 0:
            self.logEvent('英式发音按钮被点击')
        elif type == 1:
            self.logEvent('美式发音按钮被点击')
        
        bytes = webDict.query_spelling(self.currentWord, type)
        if bytes:
            self.player.play_raw(bytes)
        else:
            self.logEvent('发音查询失败')
        
    def updateWindow(self):
        pass