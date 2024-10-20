# import sys
from PyQt5.QtWidgets import QWidget, QApplication, QFrame, QHBoxLayout, QVBoxLayout
from PyQt5.QtWidgets import QScrollArea

from PyQt5.QtGui import QDesktopServices, QPainter, QPen, QColor,  QIcon
from qfluentwidgets import FluentWindow
from qfluentwidgets import NavigationItemPosition, FluentWindow, SubtitleLabel, setFont, PushButton, IconWidget
from qfluentwidgets import FluentIcon,TitleLabel,CaptionLabel,ToolButton,ToolTipFilter
from PyQt5.QtCore import Qt, QTranslator
from PyQt5.QtCore import Qt, pyqtSignal, QUrl, QEvent

from app.interface_home import MainPageWidget
from app.interface_setting import SettingPageWidget

# TODO 临时占位QFrame，后面换成自己的
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
        # have to run parent's __init__ before our logic.
        super().__init__()

        # 创建子界面，实际使用时将 Widget 换成自己的子界面
        self.homeInterface = MainPageWidget('Home', self)

        self.dbmtInterface = Widget('DBMT', self)

        self.settingInterface = SettingPageWidget("Setting",self)


        # self.reverseInterface = Widget('Mod逆向', self)
        # self.encryptionInterface = Widget('Mod加密', self)
        # self.protectInterface = Widget('资产保护', self)

        self.initNavigation()
        self.initWindow()

    def initNavigation(self):
        self.addSubInterface(self.homeInterface, FluentIcon.HOME, 'Home')
        pass
        self.addSubInterface(self.dbmtInterface, FluentIcon.CALORIES, 'Mod制作')

        # plugins will be add later.
        # self.addSubInterface(self.reverseInterface, FluentIcon.CANCEL, 'Mod逆向')
        # self.addSubInterface(self.encryptionInterface, FluentIcon.IOT, 'Mod加密')
        # self.addSubInterface(self.protectInterface, FluentIcon.VPN, '资产保护')

        self.addSubInterface(self.settingInterface, FluentIcon.SETTING, 'Settings', NavigationItemPosition.BOTTOM)

    def initWindow(self):
        # Set widnow size.
        self.resize(1000, 680)

        # We don't need this ,but might be useful so keep it here.
        # self.setMinimumWidth(600)

        # This can't show on PyQt-Fluent-Widget's window,anyway we keep it for fun.
        # self.setWindowIcon(QIcon('NicoMico.ico'))

        # Set window title.
        self.setWindowTitle('DirectX Buffer Mod Tool')

        # set window on center screen.
        desktop = QApplication.desktop().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w//2 - self.width()//2, h//2 - self.height()//2)

        # show window.
        self.show()
        
        # I don't know if this processEvents() can be deleted ,but for compatible reason we add it here.
        QApplication.processEvents()
