from layouts.main_window import MainWindow
from PyQt5.QtWidgets import QApplication
import PyQt5.QtCore as Qt

if __name__ == '__main__':
    import sys

    Qt.QCoreApplication.setAttribute(Qt.Qt.ApplicationAttribute.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())