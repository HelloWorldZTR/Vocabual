from PyQt5.QtWidgets import QFrame, QVBoxLayout, QLabel, QHBoxLayout, QWidget, QSizePolicy, QSpacerItem
import PyQt5.Qt as Qt

from qfluentwidgets import ElevatedCardWidget, ProgressRing, BodyLabel

class StaticsFrame(QFrame):
    def __init__(self, parent, unique_name):
        super().__init__(parent)
        self.setObjectName(unique_name)

        # 设置布局
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setLayout(QHBoxLayout())

        # Two Columns Layout
        self.leftLayout = QVBoxLayout()
        self.rightLayout = QVBoxLayout()

        self.layout().addLayout(self.leftLayout)
        self.layout().addLayout(self.rightLayout)

        self.prog = ProgressRingCardWidget(self)
        self.calendar = CalendatChartCardWidget(self)
        self.leftLayout.addWidget(self.prog)
        self.leftLayout.addWidget(self.calendar)
        self.leftLayout.setStretch(0, 1)

        self.kline = KlineChartCardWidget(self)
        self.rightLayout.addWidget(self.kline)
        self.rightLayout.setStretch(0, 1)




class ProgressRingCardWidget(ElevatedCardWidget):
    def __init__(self, parent=None, percentage = 0):
        super().__init__(parent)

        self.setLayout(QHBoxLayout())

        self.hspacer = QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.prog = ProgressRing(self)
        self.prog.setRange(0, 100)
        self.layout().addItem(self.hspacer)
        self.layout().addWidget(self.prog)
        self.layout().addItem(self.hspacer)

        class _InfoWidget(QWidget):
            def __init__(self, parent=None):
                super().__init__(parent)
                self.setLayout(QVBoxLayout())
                self.labelBookName = BodyLabel(self)
                self.labelWordCount = BodyLabel(self)
                self.layout().addWidget(self.labelBookName)
                self.layout().addWidget(self.labelWordCount)
                self.layout().setAlignment(Qt.Qt.AlignCenter)

        
        self.info = _InfoWidget(self)
        self.layout().addWidget(self.info)
        self.layout().addItem(self.hspacer)
        #Fill dummy Info
        self.setInfo("小学英语", 114514, 111199)
    
    def setInfo(self, bookName, wordCount, wordLearned):
        percentage = int(wordLearned / wordCount * 100)
        self.info.labelBookName.setText(bookName)
        self.info.labelWordCount.setText(f'单词数量: {wordLearned}/{wordCount}')
        self.prog.setValue(percentage)


class CalendatChartCardWidget(ElevatedCardWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setMinimumHeight(300)

        self.setLayout(QHBoxLayout())
        self.label = QLabel(self)
        self.label.setText("Calendar Chart")
        self.layout().addWidget(self.label)

class KlineChartCardWidget(ElevatedCardWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setMinimumSize(300, 300)

        self.setLayout(QHBoxLayout())
        self.label = QLabel(self)
        self.label.setText("Kline Chart")
        
        self.layout().addWidget(self.label)