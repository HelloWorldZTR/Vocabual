from qfluentwidgets import Dialog

from utils.uitools import FrameWrapper
from .Ui_recite import Ui_Frame 
from extern import webDict
from utils.audio import PlaysoundPlayer
import settings

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
        self.player = PlaysoundPlayer()
        super().__init__(Ui_Frame(), parent=parent, unique_name=unique_name)
        self.frame.ok.hide()
        self.frame.notok.hide()
        self.frame.next.hide()
        self.frame.pronounceLabel1.setText("[英]"+self.pronounceUK)
        self.frame.pronounceLabel2.setText("[美]"+self.pronounceUS)
        self.frame.wordLabel.setText(self.currentWord)
        self.frame.progressBar.setProperty('value', 0)
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
        self.addToFavourite()
        self.frame.knownButton.hide()
        self.frame.unknownButton.hide()
        self.frame.next.show()
        self.frame.explanationLabel.setText(self.currentTranslation)
    def switch_ok(self):
        self.frame.ok.hide()
        self.frame.notok.hide()
        self.frame.next.show()
    def switch_notok(self):
        self.addToFavourite()
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
            self.frame.explanationLabel.setText('')
            if settings.get_favourite_status(self.wordList[self.currentWordIndex].id):
                self.frame.favouriteButton.blockSignals(True)
                self.frame.favouriteButton.setChecked(True)
                self.frame.favouriteButton.blockSignals(False)
            else:
                self.frame.favouriteButton.blockSignals(True)
                self.frame.favouriteButton.checked = False
                self.frame.favouriteButton.blockSignals(False)
    """连接信号和槽函数"""
    def setupConnections(self):
        self.frame.favouriteButton.clicked.connect(lambda: self.addToFavourite())
        self.frame.knownButton.clicked.connect(lambda: self.switch_knownButton())
        self.frame.unknownButton.clicked.connect(lambda: self.switch_unknownButton())
        self.frame.ok.clicked.connect(lambda: self.switch_ok())
        self.frame.notok.clicked.connect(lambda: self.switch_notok())
        self.frame.next.clicked.connect(lambda: self.switch_next())
        self.frame.pronBtn1.clicked.connect(lambda: self.pronounce(0))  # 英式发音按钮
        self.frame.pronBtn2.clicked.connect(lambda: self.pronounce(1))  # 美式发音按钮

    
    def logEvent(self, text):
        print("[log] " + text)
    
    def addToFavourite(self):
        word = self.wordList[self.currentWordIndex]
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