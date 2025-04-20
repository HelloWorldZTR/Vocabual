from qfluentwidgets import NavigationItemPosition, FluentWindow, SubtitleLabel, setFont
from qfluentwidgets import FluentIcon as FIF
from PyQt5.QtWidgets import QApplication, QFrame, QHBoxLayout
from PyQt5.QtWidgets import QVBoxLayout, QWidget

import uuid

from .Ui_bookshelf import Ui_Frame as BookShelfWidget
from .Ui_favourite import Ui_Frame as FavouriteWidget
from .Ui_recite import Ui_Frame as ReciteWidget
from .Ui_review import Ui_Frame as ReviewWidget
from .Ui_statics import Ui_Frame as StatisticsWidget

class WidgetWrapper(QFrame):
    """ 用于包装子界面，避免在导航栏中显示重复的名称 """
    def __init__(self, frame, parent=None, unique_name=None):
        super().__init__(parent=parent)
        frame.setupUi(self)
        # 必须设置不重复的名称，否则会导致导航栏的图标不显示
        self.setObjectName(unique_name)


class MainWindow(FluentWindow):
    """ 主界面 """

    def __init__(self):
        super().__init__()

        # 创建子界面
        self.reciteInterface = WidgetWrapper(ReciteWidget(), self, 'reciteInterface')
        self.revirewInterface = WidgetWrapper(ReviewWidget(), self, 'revirewInterface')
        self.favouriteInterface = WidgetWrapper(FavouriteWidget(), self, 'favouriteInterface')
        self.statisticsInterface = WidgetWrapper(StatisticsWidget(), self, 'statisticsInterface')
        self.bookShelfInterface = WidgetWrapper(BookShelfWidget(), self, 'bookShelfInterface')

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


