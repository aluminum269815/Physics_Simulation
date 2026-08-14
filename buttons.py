from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import Qt


BUTTON_STYLE = """
    QPushButton {
        background-color: #f2f2f2;
        color: #1a1a1a;
        border: 2px solid #8a8a8a;
        border-radius: 10px;
        padding: 8px 20px;
        font-family: Arial;
        font-weight: bold;
        font-size: 13px;
    }
    QPushButton:hover {
        background-color: #a8a8a8;
    }
    QPushButton:disabled {
        background-color: #dcdcdc;
        color: #9a9a9a;
        border-color: #bfbfbf;
    }
"""


class FireButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__("FIRE", parent)
        self.setCursor(Qt.PointingHandCursor)
        self.setStyleSheet(BUTTON_STYLE)
        self.adjustSize()


class ResetButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__("RESET", parent)
        self.setCursor(Qt.PointingHandCursor)
        self.setStyleSheet(BUTTON_STYLE)
        self.adjustSize()