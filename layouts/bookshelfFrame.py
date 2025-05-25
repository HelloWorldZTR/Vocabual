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
    ImageLabel,
    PillPushButton
)
from qfluentwidgets import FluentIcon, TreeWidget

from PyQt5.QtWidgets import QHBoxLayout, QFrame, QVBoxLayout, QSizePolicy, QSpacerItem, QTreeWidgetItem
from PyQt5.QtCore import Qt

import bookdata
import settings

class PrevirewCard(SimpleCardWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setLayout(QVBoxLayout())
        self.setMinimumHeight(200)
        self.setMinimumWidth(200)
        self.setObjectName("previewCard")

        self.bookTitle = TitleLabel("书名", self)
        self.infoLabel = BodyLabel("书籍简介", self)
        self.infoLabel.setText("请从左侧选择一本书籍以查看详细信息。")
        self.infoLabel.setAlignment(Qt.AlignLeft)
        self.selectBtn = PrimaryPushButton("选择该书", self)

        self.layout().addWidget(self.bookTitle)
        self.layout().addWidget(self.infoLabel)
        self.layout().addWidget(self.selectBtn)

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
        self.selected_book_id = None
        

        self.treedata = bookdata.get_book_tree()
        current_selected_item = None
        for item in self.treedata:
            book_item = QTreeWidgetItem(self.treeview)
            book_item.setText(0, self.treedata[item]['title'])
            book_item.setData(0, Qt.UserRole, item)

            if settings.settings['book_id'] == item:
                current_selected_item = book_item
            
            for child in self.treedata[item]['children']:
                child_item = QTreeWidgetItem(book_item)
                child_item.setText(0, self.treedata[item]['children'][child]['title'])
                child_item.setData(0, Qt.UserRole, child)
                # 这里可以添加更多的子节点或属性9
                book_item.addChild(child_item)

                if settings.settings['book_id'] == child:
                    current_selected_item = child_item
        
        if current_selected_item is not None:
            self.treeview.setCurrentItem(current_selected_item)
            self.on_item_clicked(current_selected_item, 0)

        self.treeview.expandAll()
        self.treeview.itemClicked.connect(self.on_item_clicked)
        self.preview.selectBtn.clicked.connect(self.select_book)
        # print(self.treedata)
    
    def on_item_clicked(self, item, column):
        """
        当树形视图中的项目被点击时，更新预览卡片的内容。
        :param item: 被点击的树形项目
        :param column: 被点击的列
        """
        book_id = item.data(0, Qt.UserRole)
        book = bookdata.books[book_id]
        
        self.preview.bookTitle.setText(book.title)
        self.preview.infoLabel.setText(
"""书籍ID: {book_id}\n
单词量: {word_count}\n""".format(book_id=book_id, word_count=book.word_count)
        )
        self.selected_book_id = book_id
        print("[log] Select" + book.title)
    
    def select_book(self):
        print("[log] Selected book ID:", self.selected_book_id)
        settings.set_book_id(self.selected_book_id)
    
    def updateWindow(self):
        pass
