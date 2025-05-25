from utils.uitools import FrameWrapper
from qfluentwidgets import (
    GroupHeaderCardWidget,
    PushButton,
    ComboBox,
    SearchLineEdit,
    IconWidget,
    InfoBarIcon,
    BodyLabel,
    PrimaryPushButton,
    SimpleCardWidget,
    TitleLabel,
    ImageLabel
)
from qfluentwidgets import FluentIcon, TreeWidget

from PyQt5.QtWidgets import QHBoxLayout, QFrame, QVBoxLayout, QSizePolicy, QSpacerItem, QTreeWidgetItem
from PyQt5.QtCore import Qt

import bookdata

class PrevirewCard(SimpleCardWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setLayout(QVBoxLayout())
        self.setMinimumHeight(200)
        self.setMinimumWidth(200)
        self.setObjectName("previewCard")

        self.bookTitle = TitleLabel("书名", self)
        self.bookImg = ImageLabel(self)
        self.infoLabel = BodyLabel("书籍简介", self)
        self.infoLabel.setWordWrap(True)

        self.layout().addWidget(self.bookTitle)
        self.layout().addWidget(self.bookImg)
        self.layout().addWidget(self.infoLabel)

class BookshelfFrame(QFrame):
    def __init__(self, parent=None, unique_name=None):
        super().__init__(parent)
        self.setObjectName(unique_name)

        self.setLayout(QHBoxLayout())

        self.treeview = TreeWidget(self)
        self.layout().addWidget(self.treeview)
        self.preview = PrevirewCard(self)
        self.layout().addWidget(self.preview)
        self.treeview.setHeaderHidden(True)
        self.treeview.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        

        self.treedata = bookdata.get_book_tree()
        print(self.treedata)