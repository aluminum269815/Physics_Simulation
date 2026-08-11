import os

from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPixmap, QPainter
from PyQt5.QtCore import Qt, QPoint, QRect, pyqtSignal



lift_leg_crop = QRect(518, 628, 1257, 842)
head_crop = QRect(0, 0, 552, 179)


class Cannon(QWidget):

    moved = pyqtSignal(int)  # emits the new y position whenever it moves

    def __init__(self, parent=None,
                 pic_of_lift="asset/cannonlift&leg.png",
                 pic_of_head="asset/cannonhead.png",
                 lift_height=110, head_height=70,
                 ground_y=None, top_y=0):
        super().__init__(parent)

        raw_lift = QPixmap(os.path.abspath(pic_of_lift)).copy(lift_leg_crop)
        self.lift_pixmap = raw_lift.scaledToHeight(lift_height, Qt.SmoothTransformation)

        raw_head = QPixmap(os.path.abspath(pic_of_head)).copy(head_crop)
        self.head_pixmap = raw_head.scaledToHeight(head_height, Qt.SmoothTransformation)


        self.head_offset_x = int(self.lift_pixmap.width() * 0.35)
        self.head_offset_y = -int(self.head_pixmap.height() * 0.55)


        min_x = min(0, self.head_offset_x)
        min_y = min(0, self.head_offset_y)
        max_x = max(self.lift_pixmap.width(), self.head_offset_x + self.head_pixmap.width())
        max_y = max(self.lift_pixmap.height(), self.head_offset_y + self.head_pixmap.height())

        self._lift_draw_pos = QPoint(-min_x, -min_y)
        self._head_draw_pos = QPoint(self.head_offset_x - min_x, self.head_offset_y - min_y)

        self.setFixedSize(max_x - min_x, max_y - min_y)
        self.setCursor(Qt.OpenHandCursor)

        self._dragging = False
        self._drag_start_y = 0
        self._widget_start_y = 0


        self.ground_y = ground_y
        self.top_y = top_y

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(self._lift_draw_pos, self.lift_pixmap)
        painter.drawPixmap(self._head_draw_pos, self.head_pixmap)

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
