import sys

from PyQt5.QtCore import Qt, QTranslator
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication
from qfluentwidgets import FluentTranslator

from app.main_window import MainWindow

# DPI相关设置
# QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
# QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
# QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

if __name__ == "__main__":
    # 创建QApplication对象
    app = QApplication(sys.argv)

    # 创建主窗口
    dbmt_widnow = MainWindow()

    # 程序进入循环等待状态
    app.exec()
