from utils.uitools import FrameWrapper
from .Ui_bookshelf import Ui_Frame
from qfluentwidgets import GroupHeaderCardWidget, PushButton, ComboBox, SearchLineEdit, IconWidget, InfoBarIcon, BodyLabel, PrimaryPushButton
from qfluentwidgets import FluentIcon
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtCore import Qt

class BookshelfFrame(FrameWrapper):
    def __init__(self, parent=None, unique_name=None):
        super().__init__(Ui_Frame(), parent, unique_name)

    def setupConnections(self):
        pass

