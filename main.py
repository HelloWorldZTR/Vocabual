from layouts.Ui import MainWindow
from PyQt5.QtWidgets import QApplication
import PyQt5.QtCore as Qt
from PyQt5.QtGui import QIcon
import os

import sys

if __name__ == '__main__':
    # 开启HIDPI
    Qt.QCoreApplication.setAttribute(Qt.Qt.ApplicationAttribute.AA_EnableHighDpiScaling)

    # 启动
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    # 退出
    sys.exit(app.exec_())