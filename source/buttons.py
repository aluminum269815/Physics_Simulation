from PyQt5.QtWidgets import QPushButton
from PyQt5.QtGui import QIcon, QPainter, QColor
from PyQt5.QtCore import Qt

from constants import *
from functions import load_image


class Button(QPushButton):
    image_paths = {'default': None}
    initial_image = 'default'
    size = (100, 100)

    def __init__(self, program):
        super().__init__(program)
        
        self.images = {}
        for name, path in self.image_paths.items():
            self.images[name] = load_image(path).scaled(*self.size)
        self.image = self.images[self.initial_image]
        self.hovering = False

        self.setIcon(QIcon(self.image))
        self.setIconSize(self.image.size())
        self.setFixedSize(self.image.size())
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

    def get_darkened_image(self):
        darkened_image = self.image.copy()
        painter = QPainter(darkened_image)
        painter.setCompositionMode(QPainter.CompositionMode_SourceAtop)
        painter.fillRect(darkened_image.rect(), QColor(0, 0, 0, 70))
        painter.end()
        return darkened_image

    def update_image(self):
        if self.hovering:
            darkened_image = self.get_darkened_image()
            self.setIcon(QIcon(darkened_image))
        else:
            self.setIcon(QIcon(self.image))

    def set_image(self, image_name):
        self.image = self.images[image_name]
        self.update_image()

    def enterEvent(self, event):
        self.hovering = True
        self.update_image()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.hovering = False
        self.update_image()
        super().leaveEvent(event)


class FireButton(Button):
    image_paths = {'default': 'fire_button.png'}
    size = FIRE_BUTTON_SIZE
    

class PauseButton(Button):
    image_paths = {'playing': 'pause_button_playing.png',
                   'paused': 'pause_button_paused.png'}
    initial_image = 'playing'
    size = PAUSE_BUTTON_SIZE

class ResetButton(Button):
    image_paths = {'default': 'reset_button.png'}
    size = RESET_BUTTON_SIZE
