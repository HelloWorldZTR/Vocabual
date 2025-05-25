from utils.uitools import FrameWrapper
from PyQt5.QtWidgets import (
    QFrame,
    QVBoxLayout,
    QTableWidgetItem,
    QPushButton,
    QSizePolicy,
    QHeaderView,
)
from extern import webDict

from qfluentwidgets import TableWidget, PushButton, TeachingTip, BodyLabel, TeachingTipTailPosition

import settings


class ListFrame(QFrame):
    def __init__(self, parent=None, unique_name=None):
        super().__init__(parent)
        self.setObjectName(unique_name)

        # 设置布局
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setLayout(QVBoxLayout())

        self.wordsTable = TableWidget(self)
        self.layout().addWidget(self.wordsTable)
        self.wordsTable.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # self.wordsTable.setStyleSheet("QTableWidget {background-color: #FFFFFF;}")
        self.wordsTable.setBorderVisible(False)
        self.wordsTable.setColumnCount(5)
        self.wordsTable.setHorizontalHeaderLabels(
            ["单词", "读音", "释义", "难度", "操作"]
        )
        self.wordsTable.horizontalHeader().setSectionResizeMode(
            2, QHeaderView.Stretch
        )  # 释义列自适应宽度
        # 其余列自适应内容
        self.wordsTable.horizontalHeader().setSectionResizeMode(
            0, QHeaderView.ResizeToContents
        )
        self.wordsTable.horizontalHeader().setSectionResizeMode(
            1, QHeaderView.ResizeToContents
        )
        self.wordsTable.horizontalHeader().setSectionResizeMode(
            3, QHeaderView.ResizeToContents
        )
        self.wordsTable.horizontalHeader().setSectionResizeMode(
            4, QHeaderView.ResizeToContents
        )
        self.wordsTable.verticalHeader().setVisible(False)

        self.updateWindow()
        # self.setupConnections()

    def updateWindow(self):
        favourite_list = settings.get_favourite_list()
        data = []
        for word in favourite_list:
            data.append([
                word.word,
                f"[英]{word.phonetic_uk} [美]{word.phonetic_us}",
                word.translation,
                word.difficulty,
                None  # 操作按钮将在后续设置
            ])
        self._setData(data)
        self.setupConnections()


    def _setData(self, data):
        """
        设置数据
        data 为一个列表，包含单词、释义、统计和操作
        """
        self.wordsTable.setRowCount(len(data))
        for i, word in enumerate(data):
            self.wordsTable.setCellWidget(i, 0, BodyLabel(word[0]))
            self.wordsTable.setItem(i, 1, QTableWidgetItem(word[1]))
            self.wordsTable.setItem(i, 2, QTableWidgetItem(word[2]))
            self.wordsTable.setItem(i, 3, QTableWidgetItem(word[3]))
            self.wordsTable.setCellWidget(i, 4, PushButton("删除"))

    def setupConnections(self):
        for i in range(self.wordsTable.rowCount()):
            button = self.wordsTable.cellWidget(i, 4)
            try:
                button.clicked.disconnect()
            except TypeError:
                pass
            button.clicked.connect(lambda _, row=i: self.deleteAction(row))

        def onSelectionChanged():
            table = self.wordsTable
            selected_rows = table.selectionModel().selectedRows()
            for index in selected_rows:
                # print(f"Selected row: {index.row()}")
                item = table.cellWidget(index.row(), 0)
                if item:
                    self.showTeachingTip(item)

        self.wordsTable.selectionModel().selectionChanged.connect(onSelectionChanged)

    def deleteAction(self, i):
        print(f"Delete action for row {i}")

    def showTeachingTip(self, target):
        expl, phrs, pic = webDict.query_youdao(target.text())
        formatted_text = ""
        if expl is not None:
            for id, it in enumerate(expl):
                expl[id] = f"{id+1}. <b>{it}</b>"
            formatted_text = "<br>".join(expl)
        else :
            formatted_text = "未找到释义"
        if phrs is not None:
            formatted_text += "<br><br><b>短语:</b>"
            for hw, ex in phrs:
                formatted_text += f'<br><b>{hw}</b>: {ex}'
        else:
            pass

        TeachingTip.create(
            target=target,
            title=target.text(),
            icon=pic if pic else None,
            duration=-1,
            parent=self,
            content=formatted_text,
            tailPosition= TeachingTipTailPosition.LEFT
        )
