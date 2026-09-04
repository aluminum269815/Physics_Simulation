import os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from constants import *
from functions import load_image


class Target(QLabel):
    def __init__(self, program):
        super().__init__(program)
        self.program = program
        self.settings = program.settings

        image = load_image('target.png')
        image = image.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        self.setPixmap(image)
        self.setFixedSize(image.size())
        self.setStyleSheet("background: transparent")
        self.setCursor(Qt.OpenHandCursor)

        self.dragging = False
        self.drag_position = QPoint()

        self.update_position()

    def mousePressEvent(self, event, **kwargs):
        if event.button() == Qt.LeftButton:
            self.dragging = True
            self.drag_position = event.globalPos()
            self.setCursor(Qt.ClosedHandCursor)

    def mouseMoveEvent(self, event, **kwargs):
        if self.dragging:
            distance_change = round((event.globalPos().x() - self.drag_position.x()) / PIXELS_PER_METRE, 1)
            height_change = round((self.drag_position.y() - event.globalPos().y()) / PIXELS_PER_METRE, 1)
            self.settings.set_target_position(self.settings.target_distance + distance_change, self.settings.target_height + height_change)
            self.drag_position = event.globalPos()
            self.update_position()
            self.program.target_position_label.update_position()

    def mouseReleaseEvent(self, event, **kwargs):
        if event.button() == Qt.LeftButton:
            self.dragging = False
            self.setCursor(Qt.OpenHandCursor)

    def update_position(self):
        x = WALL_WIDTH + CANNON_WIDTH + self.settings.target_distance * PIXELS_PER_METRE - self.width() // 2
        y = self.program.height() - GROUND_HEIGHT - self.settings.target_height * PIXELS_PER_METRE - self.height() // 2
        self.move(int(x), int(y))


class TargetLabel(QLabel):
    def __init__(self, parent):
        super().__init__(parent)
        self.settings = parent.settings
        self.target = parent.target
        self.setStyleSheet("""
            background-color: rgba(255, 255, 255, 180);
            padding: 2px 6px;
            border-radius: 3px;
            font-family: Arial;
            font-weight: bold;
            font-size: 13px;
        """)

        self.update_position()

    def update_position(self):
        self.setText(f"X: {self.settings.target_distance:.2f} m, Y: {self.settings.target_height:.2f} m")
        self.adjustSize()
        x = self.target.x() + (self.target.width() // 2) - (self.width() // 2)
        y = self.target.y() + self.target.height() + 4
        self.move(x, y)
