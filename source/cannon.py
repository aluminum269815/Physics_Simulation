import math
from PyQt5.QtWidgets import QWidget, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import  QTransform

from constants import *
from functions import load_image


class CannonPlatform(QLabel):
    def __init__(self, program):
        super().__init__(program)
        self.program = program
        self.settings = self.program.settings

        self.image = load_image("cannon_platform.png")
        self.setPixmap(self.image)
        self.setFixedSize(self.image.size())
        self.setCursor(Qt.OpenHandCursor)

        self.dragging = False
        self.drag_y = None

        self.update_position()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = True
            self.drag_y = event.globalY()
            self.setCursor(Qt.ClosedHandCursor)

    def mouseMoveEvent(self, event):
        if self.dragging:
            height_change = round((self.drag_y - event.globalY()) / PIXELS_PER_METRE, 1)
            self.program.change_cannon_height(self.settings.cannon_height + height_change)
            self.drag_y = event.globalY()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = False
            self.setCursor(Qt.OpenHandCursor)

    def update_position(self):
        barrel_offset_y = (CANNON_BARREL_LENGTH - CANNON_BARREL_PIVOT_OFFSET_X) * math.sin(math.radians(self.settings.firing_angle)) \
            + CANNON_BARREL_MUZZLE_OFFSET * math.cos(math.radians(self.settings.firing_angle))
        y = self.program.height() - GROUND_HEIGHT + CANNON_BASE_HEIGHT \
            - self.settings.cannon_height * PIXELS_PER_METRE + barrel_offset_y - CANNON_BASE_PIVOT_OFFSET_Y

        self.move(WALL_WIDTH, int(y))


class CannonBase(QLabel):
    def __init__(self, program):
        super().__init__(program)
        self.program = program
        self.settings = self.program.settings

        self.image = load_image("cannon_base.png")
        self.setPixmap(self.image)
        self.setFixedSize(self.image.size())
        self.setCursor(Qt.OpenHandCursor)

        self.dragging = False
        self.drag_y = None

        self.update_position()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = True
            self.drag_y = event.globalY()
            self.setCursor(Qt.ClosedHandCursor)

    def mouseMoveEvent(self, event):
        if self.dragging:
            height_change = round((self.drag_y - event.globalY()) / PIXELS_PER_METRE, 1)
            self.program.change_cannon_height(self.settings.cannon_height + height_change)
            self.drag_y = event.globalY()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = False
            self.setCursor(Qt.OpenHandCursor)

    def update_position(self):
        barrel_offset_x = (CANNON_BARREL_LENGTH - CANNON_BARREL_PIVOT_OFFSET_X) * math.cos(math.radians(self.settings.firing_angle)) \
            - CANNON_BARREL_MUZZLE_OFFSET * math.sin(math.radians(self.settings.firing_angle))
        x = WALL_WIDTH + CANNON_WIDTH - CANNON_BASE_PIVOT_OFFSET_X - barrel_offset_x

        y = self.program.cannon_platform.y() - self.height()

        self.move(int(x), int(y))


class CannonBarrel(QLabel):
    def __init__(self, program):
        super().__init__(program)
        self.program = program
        self.settings = self.program.settings

        self.origin_image = load_image("cannon_barrel.png")
        self.image = self.origin_image
        self.setPixmap(self.image)
        self.setFixedSize(self.image.size())
        self.setCursor(Qt.OpenHandCursor)

        self.dragging = False

        self.update_angle()
        self.update_position()

    def update_angle(self):
        transform = QTransform()
        transform.rotate(- self.settings.firing_angle)
        self.image = self.origin_image.transformed(transform, Qt.SmoothTransformation)
        self.setPixmap(self.image)
        self.setFixedSize(self.image.size())

    def update_position(self):
        pivot_x = self.program.cannon_base.x() + CANNON_BASE_PIVOT_OFFSET_X
        pivot_y = self.program.cannon_base.y() + CANNON_BASE_PIVOT_OFFSET_Y

        x = pivot_x - CANNON_BARREL_PIVOT_OFFSET_X * math.cos(math.radians(self.settings.firing_angle)) \
            - (CANNON_BARREL_DIAMETER - CANNON_BARREL_PIVOT_OFFSET_Y) * math.sin(math.radians(self.settings.firing_angle))

        y = pivot_y - (CANNON_BARREL_LENGTH - CANNON_BARREL_PIVOT_OFFSET_X) * math.sin(math.radians(self.settings.firing_angle)) \
            - (CANNON_BARREL_DIAMETER - CANNON_BARREL_PIVOT_OFFSET_Y) * math.cos(math.radians(self.settings.firing_angle))

        self.move(int(x), int(y))

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = True
            self.setCursor(Qt.ClosedHandCursor)

    def mouseMoveEvent(self, event):
        if self.dragging:
            drag_pos = self.program.mapFromGlobal(event.globalPos())
            pivot_x = self.program.cannon_base.x() + CANNON_BASE_PIVOT_OFFSET_X
            pivot_y = self.program.cannon_base.y() + CANNON_BASE_PIVOT_OFFSET_Y
            angle = int(math.degrees(math.atan2(pivot_y - drag_pos.y(), drag_pos.x() - pivot_x)))
            self.program.change_dragging_firing_angle(angle)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = False
            self.setCursor(Qt.OpenHandCursor)
            self.program.cannon_platform.update_position()
            self.program.cannon_base.update_position()
            self.update_position()
