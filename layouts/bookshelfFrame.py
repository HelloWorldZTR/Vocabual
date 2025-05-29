from utils.uitools import FrameWrapper
from qfluentwidgets import (
    SearchLineEdit,
    BodyLabel,
    PrimaryPushButton,
    SimpleCardWidget,
    TitleLabel,
    TableWidget,
    CompactSpinBox,
    TreeWidget
)

from PyQt5.QtWidgets import (
    QHBoxLayout,
    QFrame,
    QVBoxLayout,
    QSizePolicy,
    QTreeWidgetItem,
    QCompleter,
    QTableWidgetItem,
    QHeaderView,
)
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
        self.wordTabel = TableWidget(self)
        self.wordTabel.setColumnCount(2)
        self.wordTabel.horizontalHeader().hide()
        self.wordTabel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.wordTabel.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)

        self.wordcountGroup = QHBoxLayout()
        self.dailyWordCountLabel = BodyLabel("每日单词量:", self)
        self.dailyWordCount = CompactSpinBox(self)
        self.dailyWordCount.setRange(1, 1000)
        self.dailyWordCount.setValue(30)
        self.wordcountGroup.addWidget(self.dailyWordCountLabel)
        self.wordcountGroup.addWidget(self.dailyWordCount)

        self.selectBtn = PrimaryPushButton("选择该书", self)

        self.layout().addWidget(self.bookTitle)
        self.layout().addWidget(self.infoLabel)
        self.layout().addWidget(self.wordTabel)
        self.layout().addLayout(self.wordcountGroup)
        self.layout().addWidget(self.selectBtn)


class BookshelfFrame(QFrame):
    def __init__(self, parent=None, unique_name=None):
        super().__init__(parent)
        self.setObjectName(unique_name)

        self.setLayout(QHBoxLayout())
        self.column1 = QVBoxLayout()
        self.layout().addLayout(self.column1)

        # Column 1: Tree View
        self.lineEdit = SearchLineEdit(self)

        self.treeview = TreeWidget(self)
        self.column1.addWidget(self.lineEdit)
        self.column1.addWidget(self.treeview)

        # Column 2: Preview Card
        self.preview = PrevirewCard(self)
        self.layout().addWidget(self.preview)
        self.treeview.setHeaderHidden(True)
        self.treeview.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.selected_book_id = None

        self.treedata = bookdata.get_book_tree()
        self.searcchdata = {}
        current_selected_item = None
        for item in self.treedata:
            book_item = QTreeWidgetItem(self.treeview)
            book_item.setText(0, self.treedata[item]["title"])
            book_item.setData(0, Qt.UserRole, item)

            if settings.settings["book_id"] == item:
                current_selected_item = book_item

            for child in self.treedata[item]["children"]:
                child_item = QTreeWidgetItem(book_item)
                child_item.setText(0, self.treedata[item]["children"][child]["title"])
                child_item.setData(0, Qt.UserRole, child)
                book_item.addChild(child_item)
                self.searcchdata[self.treedata[item]["children"][child]["title"]] = (
                    child_item
                )

                if settings.settings["book_id"] == child:
                    current_selected_item = child_item

        if current_selected_item is not None:
            self.treeview.setCurrentItem(current_selected_item)
            self.on_item_clicked(current_selected_item, 0)

        self.completer = QCompleter(self.searcchdata.keys(), self)
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.completer.setMaxVisibleItems(10)
        self.lineEdit.setCompleter(self.completer)
        self.lineEdit.setPlaceholderText("输入以搜索书籍...")

        self.treeview.expandAll()

        self.treeview.itemClicked.connect(self.on_item_clicked)
        self.preview.selectBtn.clicked.connect(self.select_book)
        self.lineEdit.searchSignal.connect(self.on_search)
        self.lineEdit.textChanged.connect(self.on_text_changed)
        # print(self.treedata)

    def _find_closest_match(self, text):
        min_lexical_distance = float("inf")
        closest_match = None
        for item in self.searcchdata.keys():
            distance = self._lexical_distance(text, item)
            if distance < min_lexical_distance:
                min_lexical_distance = distance
                closest_match = item
        return closest_match

    def _lexical_distance(self, str1, str2):
        return sum(1 for a, b in zip(str1, str2) if a != b) + abs(len(str1) - len(str2))

    def on_text_changed(self, text):
        if text:
            closest_match = self._find_closest_match(text)
            if closest_match:
                item = self.searcchdata.get(closest_match)
                self.treeview.setCurrentItem(item)
                self.on_item_clicked(item, 0)

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
单词量: {word_count}\n""".format(
                book_id=book_id, word_count=book.word_count
            )
        )
        self.preview.wordTabel.clear()
        word_list = bookdata.books[book_id].word_list
        word_list = [settings._id_to_word(word) for word in word_list]
        self.preview.wordTabel.setRowCount(len(word_list))
        for i, word in enumerate(word_list):
            self.preview.wordTabel.setItem(i, 0, QTableWidgetItem(word.word))
            self.preview.wordTabel.setItem(i, 1, QTableWidgetItem(word.translation))
        self.selected_book_id = book_id
        print("[log] Select:" + book.title)

    def on_search(self, text):
        print("[log] Search:", text)
        if text:
            item = self.searcchdata.get(text)
            if item:
                self.treeview.setCurrentItem(item)
                self.on_item_clicked(item, 0)
            else:
                print("[log] No book found for search:", text)

    def select_book(self):
        print("[log] Selected book ID:", self.selected_book_id)
        settings.set_book_id(self.selected_book_id)
        daily_word_count = self.preview.dailyWordCount.value()
        settings.set_daily_word_count(daily_word_count)

    def updateWindow(self):
        pass
