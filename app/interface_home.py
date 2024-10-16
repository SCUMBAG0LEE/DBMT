from PyQt5.QtWidgets import QWidget, QFrame, QHBoxLayout, QVBoxLayout
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QDesktopServices, QColor

from qfluentwidgets import PushButton,FluentIcon,TitleLabel,CaptionLabel


# 一个QFrame里可以有多个QWidget，所以单独的一个页面一般用QFrame来放置，里面再放多个QWidget
class WelcomeBar(QWidget):
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
        self.vBoxLayout.setAlignment(Qt.AlignLeft | Qt.AlignTop)

        # self.buttonLayout.setSpacing(4)
        self.buttonLayout.setContentsMargins(0, 0, 0, 0)
        self.buttonLayout.addWidget(self.documentButton, 0, Qt.AlignLeft)
        self.buttonLayout.addWidget(self.sourceButton, 0, Qt.AlignLeft)
        # self.buttonLayout.addStretch(1)   Stretch就是隔老远，不用打开
        self.buttonLayout.addWidget(self.supportButton, 0, Qt.AlignLeft)
        self.buttonLayout.addWidget(self.feedbackButton, 0, Qt.AlignLeft)
        self.buttonLayout.setAlignment(Qt.AlignLeft)

        # 设置四个按钮的点击事件
        self.documentButton.clicked.connect(lambda: QDesktopServices.openUrl(QUrl("https://www.yuque.com/airde/lx53p6?# 《DBMT使用手册》")))
        self.supportButton.clicked.connect(lambda: QDesktopServices.openUrl(QUrl("https://mbd.pub/o/NicoMico/work")))
        self.sourceButton.clicked.connect(lambda: QDesktopServices.openUrl(QUrl("https://github.com/StarBobis/DBMT-GUI")))
        self.feedbackButton.clicked.connect(lambda: QDesktopServices.openUrl(QUrl("https://github.com/StarBobis/DBMT-GUI/issues")))
        
        # 设置副标题的颜色
        self.subtitleLabel.setTextColor(QColor(96, 96, 96), QColor(216, 216, 216))


class MainPageWidget(QFrame):

    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)

        # 必须给子界面设置全局唯一的对象名
        self.setObjectName(text.replace(' ', '-'))

        # 设置水平布局，方便追加元素
        self.hBoxLayout = QHBoxLayout(self)
        self.hBoxLayout.addWidget(WelcomeBar("欢迎使用DBMT(DirectX Buffer Mod Tool)","专业级DirectX Mod工具箱  --NicoMico"))
        self.hBoxLayout.setAlignment(Qt.AlignTop| Qt.AlignLeft)

        
        


