from utils.uitools import FrameWrapper
from .Ui_review import Ui_Frame

class ReviewFrame(FrameWrapper):
    def __init__(self, parent=None, unique_name=None):
        super().__init__(Ui_Frame(), parent, unique_name)
    
    def updateWindow(self):
        pass
    