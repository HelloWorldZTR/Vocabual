from PyQt5.QtWidgets import QFrame

class FrameWrapper(QFrame):
    """ 用于包装子界面，避免在导航栏中显示重复的名称 """
    def __init__(self, frame: object, parent=None, unique_name=None):
        super().__init__(parent=parent)
        self.frame = frame
        self.frame.setupUi(self)
        # 必须设置不重复的名称，否则会导致导航栏的图标不显示
        self.setObjectName(unique_name)
        # 连接信号和槽函数
        self.setupConnections()
    
    def setupConnections(self):
        """ 
        连接信号和槽函数,需要在子类中实现
        但是注意，要写成`self.frame.名字.信号.connect(self.槽函数)`
        frame不可少
        """
        pass

    def updateUi(self, **kwargs):
        """ 
        更新界面,需要在子类中实现
        """
        pass