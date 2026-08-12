import os
import sys
import math

from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPixmap, QPainter, QBitmap, QRegion
from PyQt5.QtCore import Qt, QPoint, QPointF, pyqtSignal


def load_autocropped(path):
    full_path = os.path.abspath(path)
    pixmap = QPixmap(full_path)

    image = pixmap.toImage()
    mask = QBitmap.fromImage(image.createAlphaMask())
    region = QRegion(mask)
    rect = region.boundingRect()

    if rect.isValid() and not rect.isEmpty():
        pixmap = pixmap.copy(rect)

    return pixmap


class Cannon(QWidget):
    moved = pyqtSignal(int)
    head_tilt_fix = 11.87
    max_firing_angle = 80

    def __init__(self, parent=None,
                 lift_path="asset/cannonlift&leg.png",
                 head_path="asset/cannonhead.png",
                 lift_height=110, head_height=70,
                 ground_y=None, top_y=0):
        super().__init__(parent)

        raw_lift = load_autocropped(lift_path)
        self.lift_pixmap = raw_lift.scaledToHeight(lift_height, Qt.SmoothTransformation) if not raw_lift.isNull() else raw_lift

        raw_head = load_autocropped(head_path)
        self.head_pixmap = raw_head.scaledToHeight(head_height, Qt.SmoothTransformation) if not raw_head.isNull() else raw_head

        self.head_offset_x = int(self.lift_pixmap.width() * 0.35)
        self.head_offset_y = -int(self.head_pixmap.height() * 0.55)

        self.head_pivot_x = int(self.head_pixmap.width() * 0.05)
        self.head_pivot_y = int(self.head_pixmap.height() * 0.75)

        min_x = min(0, self.head_offset_x)
        min_y = min(0, self.head_offset_y)
        max_x = max(self.lift_pixmap.width(), self.head_offset_x + self.head_pixmap.width())
        max_y = max(self.lift_pixmap.height(), self.head_offset_y + self.head_pixmap.height())



        self._lift_draw_pos = QPoint(-min_x, -min_y)
        self._head_draw_pos = QPoint(self.head_offset_x - min_x, self.head_offset_y - min_y)
        self._head_pivot = QPointF(
            self._head_draw_pos.x() + self.head_pivot_x,
            self._head_draw_pos.y() + self.head_pivot_y
        )

        width = max(1, max_x - min_x)
        height = max(1, max_y - min_y)
        self.setFixedSize(width, height)
        self.setCursor(Qt.OpenHandCursor)

        self._dragging = False
        self._drag_start_y = 0
        self._widget_start_y = 0

        self.ground_y = ground_y
        self.top_y = top_y

        self.firing_angle = 0

    def set_firing_angle(self, angle_deg):
        angle_deg = max(0, min(angle_deg, self.max_firing_angle))
        self.firing_angle = angle_deg
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.SmoothPixmapTransform)

        if not self.lift_pixmap.isNull():
            painter.drawPixmap(self._lift_draw_pos, self.lift_pixmap)

        if not self.head_pixmap.isNull():
            painter.save()
            painter.translate(self._head_pivot)
            painter.rotate(self.head_tilt_fix - self.firing_angle)
            painter.translate(-self._head_pivot)
            painter.drawPixmap(self._head_draw_pos, self.head_pixmap)
            painter.restore()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._dragging = True
            self._drag_start_y = event.globalY()
            self._widget_start_y = self.y()
            self.setCursor(Qt.ClosedHandCursor)

    def mouseMoveEvent(self, event):
        if self._dragging:
            delta_y = event.globalY() - self._drag_start_y
            new_y = self._widget_start_y + delta_y

            if self.top_y is not None:
                new_y = max(new_y, self.top_y)
            if self.ground_y is not None:
                new_y = min(new_y, self.ground_y - self.height())

            self.move(self.x(), new_y)  # x never changes - vertical movement only
            self.moved.emit(new_y)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._dragging = False
            self.setCursor(Qt.OpenHandCursor)

    def moveTo(self, y):
        if self.top_y is not None:
            y = max(y, self.top_y)
        if self.ground_y is not None:
            y = min(y, self.ground_y - self.height())
        self.move(self.x(), y)
        self.moved.emit(y)