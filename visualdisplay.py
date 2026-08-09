from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class VisualDisplay(QWidget):

    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setWindowTitle("Visual Display")
        self.setFixedSize(250, 100)
        self.setStyleSheet("font-family: Arial;")

        acceleration_arrows_label = QLabel("Show Acceleration arrows")
        self.acceleration_arrows_checkbox = QCheckBox()

        velocity_arrows_label = QLabel("Show Velocity arrows")
        self.velocity_arrows_checkbox = QCheckBox()

        layout = QVBoxLayout()

        acceleration_arrows_row = QHBoxLayout()
        acceleration_arrows_row.addWidget(acceleration_arrows_label)
        acceleration_arrows_row.addWidget(self.acceleration_arrows_checkbox)

        layout.addLayout(acceleration_arrows_row)

        velocity_arrows_row = QHBoxLayout()
        velocity_arrows_row.addWidget(velocity_arrows_label)
        velocity_arrows_row.addWidget(self.velocity_arrows_checkbox)

        layout.addLayout(velocity_arrows_row)


        self.setLayout(layout)
