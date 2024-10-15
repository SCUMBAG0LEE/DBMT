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
        super().__init__()


        # 创建子界面，实际使用时将 Widget 换成自己的子界面
        self.homeInterface = MainPageWidget('Home', self)

        self.dbmtInterface = Widget('DBMT', self)

        self.reverseInterface = Widget('Mod逆向', self)
    

        self.encryptionInterface = Widget('Mod加密', self)
        
        self.protectInterface = Widget('资产保护', self)
        # wdt =  Widget('Setting Interface', self)
        # btn = PushButton(wdt)
        # btn.setText("测试")
        # 这里添加了按钮默认会放到左上角，怎么才能设置样式和位置？

        self.settingInterface = Widget('Settings', self)
        

        self.initNavigation()
        self.initWindow()

    def initNavigation(self):
        self.addSubInterface(self.homeInterface, FluentIcon.HOME, 'Home')
        pass
        self.addSubInterface(self.dbmtInterface, FluentIcon.CALORIES, 'Mod制作')

        # TODO 后续改为检测到插件再显示插件界面
        self.addSubInterface(self.reverseInterface, FluentIcon.CANCEL, 'Mod逆向')
        self.addSubInterface(self.encryptionInterface, FluentIcon.IOT, 'Mod加密')
        self.addSubInterface(self.protectInterface, FluentIcon.VPN, '资产保护')

        self.addSubInterface(self.settingInterface, FluentIcon.SETTING, 'Settings', NavigationItemPosition.BOTTOM)

    def initWindow(self):
        # 设置窗口大小
        self.resize(1000, 680)
        # 设置最小宽度
        # self.setMinimumWidth(600)

        # TODO 后续添加图标
        self.setWindowIcon(QIcon(':/NicoMico.ico'))
        self.setWindowTitle('DirectX Buffer Mod Tool V1.0.2.3')

        desktop = QApplication.desktop().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w//2 - self.width()//2, h//2 - self.height()//2)
        self.show()
        
        QApplication.processEvents()
