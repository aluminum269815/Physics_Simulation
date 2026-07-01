import os, sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from settings import Settings


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
        self.setWindowTitle("Projectile Motion sim")
        self.background = QPixmap(os.path.abspath("asset/background.png"))
        self.resize(800, 500)

    def paintEvent(self, event):
        painter = QPainter(self)
        scaled = self.background.scaled(self.size(), aspectRatioMode=2)
        painter.drawPixmap(0, 0, scaled)

program = Program()
program.run()
