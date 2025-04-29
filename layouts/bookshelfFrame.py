from utils.uitools import FrameWrapper
from .Ui_bookshelf import Ui_Frame

class BookshelfFrame(FrameWrapper):
    def __init__(self, parent=None, unique_name=None):
        super().__init__(Ui_Frame(), parent, unique_name)

    def setupConnections(self):
        pass