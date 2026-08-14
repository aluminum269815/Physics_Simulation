from PyQt5.QtWidgets import QPushButton
from PyQt5.QtGui import QIcon, QTransform
from PyQt5.QtCore import Qt

from cannon import load_autocropped


def _load_horizontal(image_path, height):
    """Loads, autocrops, and rotates a vertical button image so it reads horizontally."""
    pixmap = load_autocropped(image_path)
    if pixmap.isNull():
        return pixmap
    rotated = pixmap.transformed(QTransform().rotate(-90), Qt.SmoothTransformation)
    return rotated.scaledToHeight(height, Qt.SmoothTransformation)


class FireButton(QPushButton):
    """
    The fire button, sitting under the cannon, rotated to sit horizontally.
    Hovering swaps its image to the dark grey version in the exact same
    spot (same fixed size for both, so nothing shifts on hover).
    """

    def __init__(self, parent=None,
                 normal_image_path="asset/white fire button.png",
                 hover_image_path="asset/dark grey button.png",
                 height=50):
        super().__init__(parent)

        self._normal_pixmap = _load_horizontal(normal_image_path, height)
        self._hover_pixmap = _load_horizontal(hover_image_path, height)

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