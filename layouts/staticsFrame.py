from PyQt5.QtWidgets import QFrame, QVBoxLayout, QLabel, QHBoxLayout, QWidget, QSizePolicy
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
        self.leftLayout.setContentsMargins(0, 0, 0, 0)
        self.leftLayout.setSpacing(0)
        self.rightLayout = QVBoxLayout()
        self.rightLayout.setContentsMargins(0, 0, 0, 0)
        self.rightLayout.setSpacing(0)
        self.layout().addLayout(self.leftLayout)
        self.layout().addLayout(self.rightLayout)

        self.prog = ProgressRingCardWidget(self)
        self.leftLayout.addWidget(self.prog)



class ProgressRingCardWidget(ElevatedCardWidget):
    def __init__(self, parent=None, percentage = 0):
        super().__init__(parent)

        self.setLayout(QHBoxLayout())
        self.prog = ProgressRing(self)
        self.prog.setRange(0, 100)
        self.layout().addWidget(self.prog)

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
        self.setInfo("小学英语", 114514, 111199)
    
    def setInfo(self, bookName, wordCount, wordLearned):
        percentage = int(wordLearned / wordCount * 100)
        self.info.labelBookName.setText(bookName)
        self.info.labelWordCount.setText(f'单词数量: {wordLearned}/{wordCount}')
        self.prog.setValue(percentage)




