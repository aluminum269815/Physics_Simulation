from PyQt5.QtWidgets import QSlider
from PyQt5.QtCore import Qt

from constants import *


class VelocitySlider(QSlider):
    def __init__(self, program):
        super().__init__(Qt.Vertical, program)
        self.program = program
        self.settings = program.settings

        self.setFixedSize(100, 600)
        self.setRange(MIN_INITIAL_VELOCITY * 10, MAX_SLIDER_INITIAL_VELOCITY * 10)
        self.setValue(int(self.settings.initial_velocity * 10))

        self.sliderMoved.connect(self.change_velocity)

    def change_velocity(self, value):
        self.program.change_initial_velocity(round(value / 10, 1))

    def update_value(self):
        self.setValue(int(self.settings.initial_velocity * 10))
