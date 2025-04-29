from qfluentwidgets import NavigationItemPosition, FluentWindow, SubtitleLabel, setFont
from qfluentwidgets import FluentIcon as FIF

from .reciteFrame import ReciteFrame
from .reviewFrame import ReviewFrame
from .favouriteFrame import FavouriteFrame
from .staticsFrame import StaticsFrame
from .bookshelfFrame import BookshelfFrame


class MainWindow(FluentWindow):
    """ 主界面 """

    def __init__(self):
        super().__init__()

        # 创建子界面
        self.reciteInterface = ReciteFrame(self, 'reciteInterface')
        self.revirewInterface = ReviewFrame(self, 'revirewInterface')
        self.favouriteInterface = FavouriteFrame(self, 'favouriteInterface')
        self.statisticsInterface = StaticsFrame(self, 'statisticsInterface')
        self.bookShelfInterface = BookshelfFrame(self, 'bookShelfInterface')


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



