from utils.uitools import FrameWrapper
from .Ui_favourite import Ui_Frame

class FavouriteFrame(FrameWrapper):
    def __init__(self, parent=None, unique_name=None):
        super().__init__(Ui_Frame(), parent, unique_name)