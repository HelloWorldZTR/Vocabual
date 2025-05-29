from qfluentwidgets import NavigationItemPosition, FluentWindow, SplashScreen, setFont
from qfluentwidgets import FluentIcon as FIF
from qframelesswindow.webengine import FramelessWebEngineView
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon

import os

class MainWindow(FluentWindow):
    """ 主界面 """

    def __init__(self):
        super().__init__()
        root_dir = os.path.dirname(os.path.abspath(__file__))
        favicon_path = os.path.join(root_dir, 'favico.png')
        # print(f'Favicon path: {favicon_path}')

        self.setWindowIcon(QIcon(favicon_path))
        self.splashScreen = SplashScreen(self.windowIcon(), self, True)
        self.splashScreen.setIconSize(QSize(102, 102))
        self.show()

        # 创建子界面
        from .reciteFrame import ReciteFrame
        from .listFrame import ListFrame
        from .reviewFrame import ReviewFrame
        from .staticsFrame import StaticsFrame
        from .bookshelfFrame import BookshelfFrame

        self.reciteInterface = ReciteFrame(self, 'reciteInterface')
        self.listInterface = ListFrame(self, 'listInterface')
        self.reviewInterface = ReviewFrame(self, 'reviewInterface')
        self.statisticsInterface = StaticsFrame(self, 'statisticsInterface')
        self.bookShelfInterface = BookshelfFrame(self, 'bookShelfInterface')


        self.initNavigation()
        self.initWindow()

        self.stackedWidget.currentChanged.connect(lambda: self.stackedWidget.currentWidget().updateWindow())

        self.splashScreen.finish()
    def initNavigation(self):
        # 设置导航栏的标题和图标
        self.addSubInterface(self.reciteInterface, FIF.HOME, '背单词', NavigationItemPosition.TOP)
        self.addSubInterface(self.reviewInterface, FIF.CALENDAR, '复习单词', NavigationItemPosition.TOP)
        self.addSubInterface(self.listInterface, FIF.BOOK_SHELF, '单词本', NavigationItemPosition.TOP)
        self.addSubInterface(self.statisticsInterface, FIF.IOT, '统计信息', NavigationItemPosition.TOP)


        self.navigationInterface.addSeparator()

        self.addSubInterface(self.bookShelfInterface, FIF.DICTIONARY, '选择辞书', NavigationItemPosition.BOTTOM)

    def initWindow(self):
        # 设置窗口的标题和图标
        self.resize(900, 700)
        # self.setWindowIcon(QIcon(':/qfluentwidgets/images/logo.png'))
        self.setWindowTitle('Vocalbul')



