from PyQt5.QtWidgets import QSlider
from PyQt5.QtCore import Qt

from constants import *


class Timeline(QSlider):
    def __init__(self, program):
        super().__init__(Qt.Horizontal, program)
        self.program = program
        self.settings = program.settings

        self.setFixedSize(1000, 100)
        self.setRange(0, 0)
        self.setEnabled(False)

        self.sliderMoved.connect(self.change_time)

    def update_value(self):
        self.setValue(int(self.settings.time // FRAME_INTERVAL))
        self.setMaximum(int(self.settings.max_time // FRAME_INTERVAL))
        self.setEnabled(self.settings.max_time > 0)

    def change_time(self, time):
        self.program.pause()
        self.program.change_time(round(time * FRAME_INTERVAL, 3))
