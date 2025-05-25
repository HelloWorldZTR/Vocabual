from utils.uitools import FrameWrapper
from .Ui_recite import Ui_Frame 
from extern import webDict
from utils.audio import PlaysoundPlayer

class ReciteFrame(FrameWrapper):
    """ 背单词界面初始化 """
    def __init__(self, parent=None, unique_name=None):
        self.wordList = []
        self.cur = -1
        self.currentWord = 'abandon'
        self.player = PlaysoundPlayer()
        super().__init__(Ui_Frame(), parent=parent, unique_name=unique_name)
        self.frame.ok.hide()
        self.frame.notok.hide()
        self.frame.next.hide()

    """不同按钮"""
    def switch_knownButton(self):
        self.frame.knownButton.hide()
        self.frame.unknownButton.hide()
        self.frame.ok.show()
        self.frame.notok.show()
        self.frame.explanationLabel.setText("v.放弃；抛弃；废弃；遗弃\n"
"n.放肆；狂热；任性；恣意任性")
    def switch_unknownButton(self):
        self.frame.knownButton.hide()
        self.frame.unknownButton.hide()
        self.frame.next.show()
        self.frame.explanationLabel.setText("v.放弃；抛弃；废弃；遗弃\n"
"n.放肆；狂热；任性；恣意任性")
    def switch_ok(self):
        self.frame.ok.hide()
        self.frame.notok.hide()
        self.frame.next.show()
    def switch_notok(self):
        self.frame.ok.hide()
        self.frame.notok.hide()
        self.frame.next.show()
    def switch_next(self):
        self.frame.ok.hide()
        self.frame.notok.hide()
        self.frame.next.hide()
        self.frame.knownButton.show()
        self.frame.unknownButton.show()
        self.frame.explanationLabel.setText("下一个")
    """连接信号和槽函数"""
    def setupConnections(self):
        self.frame.favouriteButton.clicked.connect(lambda: self.logEvent('添加到收藏夹'))
        #self.frame.knownButton.clicked.connect(lambda: self.frame.wordLabel.setText('Banana'))
        self.frame.knownButton.clicked.connect(lambda: self.switch_knownButton())
        self.frame.unknownButton.clicked.connect(lambda: self.switch_unknownButton())
        self.frame.ok.clicked.connect(lambda: self.switch_ok())
        self.frame.notok.clicked.connect(lambda: self.switch_notok())
        self.frame.next.clicked.connect(lambda: self.switch_next())
        self.frame.pronBtn1.clicked.connect(lambda: self.pronounce(0))  # 英式发音按钮
        self.frame.pronBtn2.clicked.connect(lambda: self.pronounce(1))  # 美式发音按钮


    """更新UI"""
    def updateUi(self, mode, word, percent):
        pass

    def setWord(self, word):
        pass
    
    def logEvent(self, text):
        print("[log] " + text)
    
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
        
