from qfluentwidgets import NavigationItemPosition, FluentWindow, SubtitleLabel, setFont
from qfluentwidgets import FluentIcon as FIF
from PyQt5.QtWidgets import QApplication, QFrame, QHBoxLayout
from PyQt5.QtWidgets import QVBoxLayout, QWidget

import uuid

from .Ui_bookshelf import Ui_Frame as BookShelfFrame
from .Ui_favourite import Ui_Frame as FavouriteFrame
from .Ui_recite import Ui_Frame as ReciteFrame
from .Ui_review import Ui_Frame as ReviewFrame
from .Ui_statics import Ui_Frame as StatisticsFrame

from utils.background import getTodayWallpaper

class WidgetWrapper(QFrame):
    """ 用于包装子界面，避免在导航栏中显示重复的名称 """
    def __init__(self, frame: object, parent=None, unique_name=None):
        super().__init__(parent=parent)
        self.frame = frame
        self.frame.setupUi(self)
        # 必须设置不重复的名称，否则会导致导航栏的图标不显示
        self.setObjectName(unique_name)
        # 连接信号和槽函数
        self.setupConnections()
    
    def setupConnections(self):
        """ 
        连接信号和槽函数,需要在子类中实现
        但是注意，要写成`self.frame.名字.信号.connect(self.槽函数)`
        frame不可少
        """
        pass

class ReciteWidget(WidgetWrapper, QFrame):
    """ 背单词界面的逻辑 """
    def __init__(self, parent=None):
        super().__init__(ReciteFrame(), parent=parent, unique_name="reciteInterface")

    def setupConnections(self):
        self.frame.favouriteButton.clicked.connect(lambda: self.logEvent('添加到收藏夹'))
        self.frame.knownButton.clicked.connect(lambda: self.logEvent('已知单词'))
        self.frame.unknownButton.clicked.connect(lambda: self.logEvent('未知单词'))
        self.frame.pushButton.clicked.connect(lambda: self.logEvent('发音'))

    def updateScreen(self, mode, word, percent):
        pass

    def setWord(self, word):
        pass
    
    def logEvent(self, text):
        print(text)


class MainWindow(FluentWindow):
    """ 主界面 """

    def __init__(self):
        super().__init__()

        # 创建子界面
        self.reciteInterface = ReciteWidget(self)
        self.revirewInterface = WidgetWrapper(ReviewFrame(), self, 'revirewInterface')
        self.favouriteInterface = WidgetWrapper(FavouriteFrame(), self, 'favouriteInterface')
        self.statisticsInterface = WidgetWrapper(StatisticsFrame(), self, 'statisticsInterface')
        self.bookShelfInterface = WidgetWrapper(BookShelfFrame(), self, 'bookShelfInterface')

        self.initNavigation()
        self.initWindow()

    def initNavigation(self):
        # 设置导航栏的标题和图标
        self.addSubInterface(self.reciteInterface, FIF.HOME, '背单词', NavigationItemPosition.TOP)
        self.addSubInterface(self.revirewInterface, FIF.CALENDAR, '复习单词', NavigationItemPosition.TOP)
        self.addSubInterface(self.favouriteInterface, FIF.BOOK_SHELF, '单词本', NavigationItemPosition.TOP)
        self.addSubInterface(self.statisticsInterface, FIF.IOT, '统计信息', NavigationItemPosition.TOP)


        self.navigationInterface.addSeparator()

        self.addSubInterface(self.bookShelfInterface, FIF.DICTIONARY, '选择辞书', NavigationItemPosition.BOTTOM)

    def initWindow(self):
        # 设置窗口的标题和图标
        self.resize(900, 700)
        # self.setWindowIcon(QIcon(':/qfluentwidgets/images/logo.png'))
        self.setWindowTitle('Vocalbul')


