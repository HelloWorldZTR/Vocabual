from utils.uitools import FrameWrapper
from .Ui_recite import Ui_Frame 

class ReciteFrame(FrameWrapper):
    """ 背单词界面的逻辑 """
    def __init__(self, parent=None, unique_name=None):
        super().__init__(Ui_Frame(), parent=parent, unique_name=unique_name)

    def setupConnections(self):
        self.frame.favouriteButton.clicked.connect(lambda: self.logEvent('添加到收藏夹'))
        self.frame.knownButton.clicked.connect(lambda: self.logEvent('已知单词'))
        self.frame.unknownButton.clicked.connect(lambda: self.logEvent('未知单词'))
        self.frame.pushButton.clicked.connect(lambda: self.logEvent('发音'))

    def updateUi(self, mode, word, percent):
        pass

    def setWord(self, word):
        pass
    
    def logEvent(self, text):
        print(text)
