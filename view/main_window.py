# import sys
from PyQt5.QtWidgets import QWidget, QApplication, QFrame, QHBoxLayout, QVBoxLayout
from PyQt5.QtWidgets import QScrollArea

from PyQt5.QtGui import QDesktopServices, QPainter, QPen, QColor,  QIcon
from qfluentwidgets import FluentWindow
from qfluentwidgets import NavigationItemPosition, FluentWindow, SubtitleLabel, setFont, PushButton, IconWidget
from qfluentwidgets import FluentIcon,TitleLabel,CaptionLabel,ToolButton,ToolTipFilter
from PyQt5.QtCore import Qt, QTranslator
from PyQt5.QtCore import Qt, pyqtSignal, QUrl, QEvent



class ToolBar(QWidget):
    """ Tool bar """
    def __init__(self, title, subtitle, parent=None):
        super().__init__(parent=parent)
        self.titleLabel = TitleLabel(title, self)
        self.subtitleLabel = CaptionLabel(subtitle, self)
        self.documentButton = PushButton(
            self.tr('DBMT使用文档'), self, FluentIcon.DOCUMENT)
        self.sourceButton = PushButton(self.tr('源代码'), self, FluentIcon.GITHUB)
        self.supportButton = PushButton(self.tr('赞助作者'), self, FluentIcon.HEART)
        self.feedbackButton = PushButton(self.tr('提交issue'), self, FluentIcon.FEEDBACK)

        self.vBoxLayout = QVBoxLayout(self)
        self.buttonLayout = QHBoxLayout()

        self.__initWidget()

    def __initWidget(self):
        self.setFixedHeight(138)
        self.vBoxLayout.setSpacing(0)
        self.vBoxLayout.setContentsMargins(36, 22, 36, 12)
        self.vBoxLayout.addWidget(self.titleLabel)
        self.vBoxLayout.addSpacing(4)
        self.vBoxLayout.addWidget(self.subtitleLabel)
        self.vBoxLayout.addSpacing(4)
        self.vBoxLayout.addLayout(self.buttonLayout, 1)
        self.vBoxLayout.setAlignment(Qt.AlignTop)

        self.buttonLayout.setSpacing(4)
        self.buttonLayout.setContentsMargins(0, 0, 0, 0)
        self.buttonLayout.addWidget(self.documentButton, 0, Qt.AlignLeft)
        self.buttonLayout.addWidget(self.sourceButton, 0, Qt.AlignLeft)
        # self.buttonLayout.addStretch(1)
        self.buttonLayout.addWidget(self.supportButton, 0, Qt.AlignLeft)
        self.buttonLayout.addWidget(self.feedbackButton, 0, Qt.AlignLeft)
        self.buttonLayout.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)

        self.supportButton.installEventFilter(ToolTipFilter(self.supportButton))
        self.feedbackButton.installEventFilter(
            ToolTipFilter(self.feedbackButton))

        # 设置四个按钮的点击事件
        self.documentButton.clicked.connect(
            lambda: QDesktopServices.openUrl(QUrl("https://www.yuque.com/airde/lx53p6?# 《DBMT使用手册》")))
        
        self.supportButton.clicked.connect(lambda: QDesktopServices.openUrl(QUrl("https://mbd.pub/o/NicoMico/work")))
        self.sourceButton.clicked.connect(
            lambda: QDesktopServices.openUrl(QUrl("https://github.com/StarBobis/DBMT-GUI")))
        self.feedbackButton.clicked.connect(
            lambda: QDesktopServices.openUrl(QUrl("https://github.com/StarBobis/DBMT-GUI/issues")))

        self.subtitleLabel.setTextColor(QColor(96, 96, 96), QColor(216, 216, 216))


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

class MainPageWidget(QFrame):

    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        self.hBoxLayout = QHBoxLayout(self)
        self.hBoxLayout.addWidget(ToolBar("欢迎使用DirectX Buffer Mod Tool(DBMT)","此工具献给所有热爱游戏Mod的玩家们  --NicoMico"))
        # 必须给子界面设置全局唯一的对象名
        self.setObjectName(text.replace(' ', '-'))


class MainWindow(FluentWindow):

    def __init__(self):
        super().__init__()


        # 创建子界面，实际使用时将 Widget 换成自己的子界面
        self.homeInterface = MainPageWidget('欢迎使用DirectX Buffer Mod Tool (DBMT)', self)

        self.reverseInterface = Widget('Mod逆向', self)
    

        self.encryptionInterface = Widget('Mod加密', self)
        
        self.protectInterface = Widget('资产保护', self)
        wdt =  Widget('Setting Interface', self)
        btn = PushButton(wdt)
        btn.setText("测试")
        # 这里添加了按钮默认会放到左上角，怎么才能设置样式和位置？

        self.settingInterface = wdt
        

        self.initNavigation()
        self.initWindow()

    def initNavigation(self):
        self.addSubInterface(self.homeInterface, FluentIcon.HOME, '主页')


        self.addSubInterface(self.reverseInterface, FluentIcon.CANCEL, 'Mod逆向')
        self.addSubInterface(self.encryptionInterface, FluentIcon.IOT, 'Mod加密')
        self.addSubInterface(self.protectInterface, FluentIcon.VPN, '资产保护')
        self.addSubInterface(self.settingInterface, FluentIcon.SETTING, '设置', NavigationItemPosition.BOTTOM)

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
