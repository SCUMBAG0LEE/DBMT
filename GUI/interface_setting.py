from PyQt5.QtWidgets import QWidget, QFrame, QHBoxLayout, QVBoxLayout,QLabel
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QDesktopServices, QColor,QFont

from qfluentwidgets import PushButton,FluentIcon,TitleLabel,CaptionLabel, EditableComboBox

# Choose which game to make mod.
class ChooseGameWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.HBoxLayout = QHBoxLayout(self)
        self.HBoxLayout.setSpacing(0)

        self.comboBox = EditableComboBox()
        self.comboBox.addItems([
            self.tr('GI'),
            self.tr('HSR'),
            self.tr("HI3"),
            self.tr('ZZZ'),
        ])
        self.comboBox.setPlaceholderText(self.tr('Choose your stand'))
        # self.comboBox.setMinimumWidth(100)



        # 设置字体为楷体，大小为16
        font = QFont("Microsoft YaHei", 12)
        game_name_label = QLabel("选择游戏名称",self)
        game_name_label.setFont(font)
        # game_name_label.setMinimumWidth(100)
        
        self.HBoxLayout.addWidget(game_name_label)
        self.HBoxLayout.addWidget(self.comboBox)
        self.setFixedHeight(138)


class SettingPageWidget(QFrame):

    def __init__(self, text: str, parent=None):
        # we have to run parent's __init__ function before our logic.
        super().__init__(parent=parent)

        # 必须给子界面设置全局唯一的对象名
        self.setObjectName(text.replace(' ', '-'))

        # 设置水平布局，方便追加元素
        self.VBoxLayout = QVBoxLayout(self)
        self.VBoxLayout.setAlignment(Qt.AlignTop| Qt.AlignLeft)

        # add choose game widget
        self.VBoxLayout.addWidget(ChooseGameWidget())
