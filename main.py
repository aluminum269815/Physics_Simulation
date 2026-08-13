import os, sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from settings import Settings
from constants import *


class Program:
    def __init__(self):
        self.settings = Settings()
        self.app = QApplication(sys.argv)
        self.window = Window()

    def run(self):
        self.window.show()
        sys.exit(self.app.exec_())


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Projectile Motion Simulation")
        self.background = QPixmap(os.path.abspath("assets/background.png"))
        self.resize(DEFAULT_WINDOW_WIDTH, DEFAULT_WINDOW_HEIGHT)

    def paintEvent(self, event, **kwargs):
        painter = QPainter(self)
        scaled_background = self.background.scaled(self.size(), aspectRatioMode=2)
        painter.drawPixmap(0, 0, scaled_background)

if __name__ == '__main__':
    program = Program()
    program.run()
