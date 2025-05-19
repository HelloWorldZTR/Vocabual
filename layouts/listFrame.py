from utils.uitools import FrameWrapper
from PyQt5.QtWidgets import QFrame, QVBoxLayout, QTableWidgetItem, QPushButton, QSizePolicy, QHeaderView


from qfluentwidgets import TableWidget, PushButton

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
        self.wordsTable.setHorizontalHeaderLabels(['单词', '读音', '释义', '统计', '操作'])
        self.wordsTable.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch) # 释义列自适应宽度
        # 其余列自适应内容
        self.wordsTable.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.wordsTable.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.wordsTable.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.wordsTable.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeToContents)
        self.wordsTable.verticalHeader().setVisible(False)

        # 测试用
        _data = [
            ("apple","哎朋友", "苹果苹果苹果苹果苹果苹果苹果苹果苹果...苹果苹果", "0/10", "删除"),
            ("banana","把拿拿", "香蕉香蕉香蕉香蕉香蕉香蕉香蕉香蕉香蕉香蕉...", "0/10", "删除"),
            ("orange","欧润吉", "橘子香蕉香蕉香蕉香蕉香蕉香蕉香蕉香蕉香蕉..香蕉", "0/10", "删除"),
            ("grape","sss", "葡萄", "0/10", "删除"),
            ("watermelon","sss", "香蕉香蕉香蕉香蕉香蕉香蕉香蕉", "0/10", "删除"),
        ]
        self.setData(_data)
        
    
    def setData(self, data):
        """
        设置数据
        data 为一个列表，包含单词、释义、统计和操作
        """
        self.wordsTable.setRowCount(len(data))
        for i, word in enumerate(data):
            self.wordsTable.setItem(i, 0, QTableWidgetItem(word[0]))
            self.wordsTable.setItem(i, 1, QTableWidgetItem(word[1]))
            self.wordsTable.setItem(i, 2, QTableWidgetItem(word[2]))
            self.wordsTable.setItem(i, 3, QTableWidgetItem(word[3]))
            self.wordsTable.setCellWidget(i, 4, PushButton("删除"))

    def setupConnections(self):
        for i in range(self.wordsTable.rowCount()):
            button = self.wordsTable.cellWidget(i, 4)
            button.clicked.connect(lambda _, row=i: self.deleteAction(row))

    def deleteAction(self, i):
        print(f"Delete action for row {i}")