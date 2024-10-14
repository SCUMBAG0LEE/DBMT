# import sys
from PyQt5.QtWidgets import QWidget, QApplication, QFrame, QHBoxLayout
from qfluentwidgets import FluentWindow
from PyQt5.QtGui import QIcon
from qfluentwidgets import NavigationItemPosition, FluentWindow, SubtitleLabel, setFont
from qfluentwidgets import FluentIcon as FIF
from PyQt5.QtCore import Qt, QTranslator

class Widget(QFrame):

    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        self.label = SubtitleLabel(text, self)
        self.hBoxLayout = QHBoxLayout(self)

        setFont(self.label, 24)
        self.label.setAlignment(Qt.AlignCenter)
        self.hBoxLayout.addWidget(self.label, 1, Qt.AlignCenter)

        # 必须给子界面设置全局唯一的对象名
        self.setObjectName(text.replace(' ', '-'))


class MainWindow(FluentWindow):

    def __init__(self):
        super().__init__()


        # 创建子界面，实际使用时将 Widget 换成自己的子界面
        self.homeInterface = Widget('欢迎使用DirectX Buffer Mod Tool (DBMT)', self)
        self.settingInterface = Widget('Setting Interface', self)


        self.initNavigation()
        self.initWindow()

    def initNavigation(self):
        self.addSubInterface(self.homeInterface, FIF.HOME, 'Home')

        self.addSubInterface(self.settingInterface, FIF.SETTING, 'Settings', NavigationItemPosition.BOTTOM)

    def initWindow(self):
        # 设置窗口大小
        self.resize(1200, 680)
        # 设置最小宽度
        self.setMinimumWidth(800)
        self.setWindowIcon(QIcon(':/NicoMico.ico'))
        self.setWindowTitle('DirectX Buffer Mod Tool V1.0.2.2')

        # self.setMicaEffectEnabled(cfg.get(cfg.micaEnabled))

        # create splash screen
        # self.splashScreen = SplashScreen(self.windowIcon(), self)
        # self.splashScreen.setIconSize(QSize(106, 106))
        # self.splashScreen.raise_()

        desktop = QApplication.desktop().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w//2 - self.width()//2, h//2 - self.height()//2)
        self.show()
        QApplication.processEvents()
