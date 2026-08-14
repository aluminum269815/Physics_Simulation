from PyQt5.QtWidgets import QPushButton
from PyQt5.QtGui import QIcon, QTransform, QPainter, QColor
from PyQt5.QtCore import Qt

from cannon import load_autocropped


def _load_horizontal(image_path, height):
    pixmap = load_autocropped(image_path)
    if pixmap.isNull():
        return pixmap
    rotated = pixmap.transformed(QTransform().rotate(90), Qt.SmoothTransformation)
    return rotated.scaledToHeight(height, Qt.SmoothTransformation)


def _darkened(pixmap):
    result = pixmap.copy()
    painter = QPainter(result)
    painter.setCompositionMode(QPainter.CompositionMode_SourceAtop)
    painter.fillRect(result.rect(), QColor(0, 0, 0, 70))
    painter.end()
    return result


class FireButton(QPushButton):
    def __init__(self, parent=None, image_path="assets/white fire button.png", height=50):
        super().__init__(parent)

        self._normal_pixmap = _load_horizontal(image_path, height)
        self._hover_pixmap = _darkened(self._normal_pixmap) if not self._normal_pixmap.isNull() else self._normal_pixmap

        self.setIcon(QIcon(self._normal_pixmap))
        self.setIconSize(self._normal_pixmap.size())
        self.setFixedSize(self._normal_pixmap.width() + 6, self._normal_pixmap.height() + 6)
        self.setCursor(Qt.PointingHandCursor)
        self.setStyleSheet("""
            QPushButton {
                border: none;
                background: transparent;
            }
            QPushButton:disabled {
                background: rgba(0, 0, 0, 30);
                border-radius: 6px;
            }
        """)

    def enterEvent(self, event):
        if not self._hover_pixmap.isNull():
            self.setIcon(QIcon(self._hover_pixmap))
        super().enterEvent(event)

    def leaveEvent(self, event):
        if not self._normal_pixmap.isNull():
            self.setIcon(QIcon(self._normal_pixmap))
        super().leaveEvent(event)


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

class ResetButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__("RESET", parent)
        self.setCursor(Qt.PointingHandCursor)
        self.setStyleSheet(BUTTON_STYLE)
        self.adjustSize()