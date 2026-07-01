import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from settings import Settings


class Program(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Projectile Motion sim")
        self.background = QPixmap("H:/Untitled design.png")
        self.resize(800, 500)
        self.settings = Settings()

    def paintEvent(self, event):
        painter = QPainter(self)
        scaled = self.background.scaled(self.size(), aspectRatioMode=2)
        painter.drawPixmap(0, 0, scaled)

app = QApplication(sys.argv)
window = Program()
window.show()
sys.exit(app.exec_())
