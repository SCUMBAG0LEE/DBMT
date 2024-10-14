

import sys
from PyQt5.QtWidgets import QWidget, QApplication

app = QApplication(sys.argv)
widget = QWidget()
widget.resize(640, 480)
widget.setWindowTitle("DirectX Buffer Mod Tool V1.0.2.2")
widget.show()
sys.exit(app.exec())