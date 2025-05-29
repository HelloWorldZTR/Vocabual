from qfluentwidgets import Dialog
from utils.uitools import FrameWrapper
from .Ui_review import Ui_Frame 
from PyQt5.QtCore import QTimer
import settings
import random
import bookdata

class ReviewFrame(FrameWrapper):
    """ 背单词界面初始化 """
    def __init__(self, parent=None, unique_name=None):
        super().__init__(Ui_Frame(), parent=parent, unique_name=unique_name)
        self.root = parent
        self.wordList = settings.get_favourite_list()
        self.buttons = [None, self.frame.A, self.frame.B, self.frame.C, self.frame.D]
        if len(self.wordList) == 0:
            self.frame.wordLabel_2.setText('没有单词可以复习啦！')
            for i in range(1, 5):
                self.buttons[i].hide()
            return
        random.shuffle(self.wordList)  # 随机打乱单词列表
        # self.otherWordList = list(bookdata.words.values())
        self.otherWordList = bookdata.books[settings.settings['book_id']].word_list
        self.otherWordList = [settings._id_to_word(word_id) for word_id in self.otherWordList]
        #print(type(self.otherWordList))
        self.currentWordIndex = 0
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
                    while True:
                        randomWord = random.choice(self.otherWordList)
                        if randomWord.translation != self.currentTranslation and randomWord.translation != "暂无翻译":
                            break
                    self.buttons[i].setText(randomWord.translation)
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
            self.frame.wordLabel_2.setText('今日复习任务已经完成啦！😀')
            for i in range(1, 5):
                self.buttons[i].hide()
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
                        while True:
                            randomWord = random.choice(self.otherWordList)
                            if randomWord.translation != self.currentTranslation and randomWord.translation != "暂无翻译":
                                break
                        self.buttons[i].setText(randomWord.translation)
            else:
                self.frame.wordLabel_2.setText(self.currentTranslation)
                for i in range(1, 5):
                    if i == self.answer:
                        self.buttons[i].setText(self.currentWord)
                    else:
                        self.buttons[i].setText((random.choice(self.otherWordList)).word)
    """还原按钮"""
    def resetButton(self):
        for i in range(1, 5):
            self.buttons[i].setStyleSheet("color: black;")
    """不同按钮"""
    def onClickButton(self, id:int):
        if id == self.answer:
            self.buttons[id].setText( self.buttons[id].text() + " ✔")
            self.buttons[id].setStyleSheet("color: green;")
            settings.set_reviewed(self.wordList[self.currentWordIndex].id)
            self.logEvent(f'单词 {self.wordList[self.currentWordIndex].word} 已复习')
        else:
            self.buttons[id].setText( self.buttons[id].text() + " ✘")
            self.buttons[self.answer].setText( self.buttons[self.answer].text() + " ✔")
            self.buttons[id].setStyleSheet("color: red;")
            self.buttons[self.answer].setStyleSheet("color: green;")
        QTimer.singleShot(2000, self.nextWord)
    
        
    """连接信号和槽函数"""
    def setupConnections(self):
        self.frame.A.clicked.connect(lambda: self.onClickButton(1))
        self.frame.B.clicked.connect(lambda: self.onClickButton(2))
        self.frame.C.clicked.connect(lambda: self.onClickButton(3))
        self.frame.D.clicked.connect(lambda: self.onClickButton(4))

    def logEvent(self, text):
        print("[log] " + text)
        
    def updateWindow(self):
        self.wordList = settings.get_favourite_list()
        if len(self.wordList) == 0:
            self.frame.wordLabel_2.setText('没有单词可以复习啦！')
            for i in range(1, 5):
                self.buttons[i].hide()
            return
        random.shuffle(self.wordList)  # 随机打乱单词列表
        self.otherWordList = list(bookdata.words.values())
        #print(type(self.otherWordList))
        self.currentWordIndex = 0
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
                    while True:
                        randomWord = random.choice(self.otherWordList)
                        if randomWord.translation != self.currentTranslation and randomWord.translation != "暂无翻译":
                            break
                    self.buttons[i].setText(randomWord.translation)
        else:
            self.frame.wordLabel_2.setText(self.currentTranslation)
            for i in range(1, 5):
                if i == self.answer:
                    self.buttons[i].setText(self.currentWord)
                else:
                    self.buttons[i].setText((random.choice(self.otherWordList)).word)