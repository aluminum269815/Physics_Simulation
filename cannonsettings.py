from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class CannonSettings(QWidget):

    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setWindowTitle("Cannon Settings")
        self.setFixedSize(350, 250)

        initial_velocity_label = QLabel("Initial Velocity")

        self.initial_velocity_slider = QSlider(Qt.Horizontal)
        self.initial_velocity_slider.setMinimum(0)
        self.initial_velocity_slider.setMaximum(100000)
        self.initial_velocity_slider.setValue(0)

        self.initial_velocity_input = QLineEdit()
        self.initial_velocity_input.setText("0")
        self.initial_velocity_input.setFixedWidth(60)


        cannonball_mass_label = QLabel("Cannonball Mass")

        self.cannonball_mass_slider = QSlider(Qt.Horizontal)
        self.cannonball_mass_slider.setMinimum(0)
        self.cannonball_mass_slider.setMaximum(100000)
        self.cannonball_mass_slider.setValue(0)

        self.cannonball_mass_input = QLineEdit()
        self.cannonball_mass_input.setText("0")
        self.cannonball_mass_input.setFixedWidth(60)

        cannon_height_label = QLabel("Cannon Height")

        self.cannon_height_slider = QSlider(Qt.Horizontal)
        self.cannon_height_slider.setMinimum(0)
        self.cannon_height_slider.setMaximum(100000)
        self.cannon_height_slider.setValue(0)

        self.cannon_height_input = QLineEdit()
        self.cannon_height_input.setText("0")
        self.cannon_height_input.setFixedWidth(60)

        cannonball_radius_label = QLabel("Cannon Radius")

        self.cannonball_radius_slider = QSlider(Qt.Horizontal)
        self.cannonball_radius_slider.setMinimum(0)
        self.cannonball_radius_slider.setMaximum(100000)
        self.cannonball_radius_slider.setValue(0)

        self.cannonball_radius_input = QLineEdit()
        self.cannonball_radius_input.setText("0")
        self.cannonball_radius_input.setFixedWidth(60)

        firing_angle_label = QLabel("Firing Angle")

        self.firing_angle_slider = QSlider(Qt.Horizontal)
        self.firing_angle_slider.setMinimum(0)
        self.firing_angle_slider.setMaximum(100000)
        self.firing_angle_slider.setValue(0)

        self.firing_angle_input = QLineEdit()
        self.firing_angle_input.setText("0")
        self.firing_angle_input.setFixedWidth(60)

        self.initial_velocity_slider.valueChanged.connect(self.update_initial_velocity)
        self.initial_velocity_input.editingFinished.connect(self.change_initial_velocity)

        self.cannonball_mass_slider.valueChanged.connect(self.update_cannonball_mass)
        self.cannonball_mass_input.editingFinished.connect(self.change_cannonball_mass)

        self.cannon_height_slider.valueChanged.connect(self.update_cannon_height)
        self.cannon_height_input.editingFinished.connect(self.change_cannon_height)

        self.cannonball_radius_slider.valueChanged.connect(self.update_cannonball_radius)
        self.cannonball_radius_input.editingFinished.connect(self.change_cannonball_radius)

        self.firing_angle_slider.valueChanged.connect(self.update_firing_angle)
        self.firing_angle_input.editingFinished.connect(self.change_firing_angle)

        layout = QVBoxLayout()

        layout.addWidget(initial_velocity_label)

        initial_velocity_row = QHBoxLayout()
        initial_velocity_row.addWidget(self.initial_velocity_slider)
        initial_velocity_row.addWidget(self.initial_velocity_input)

        layout.addLayout(initial_velocity_row)

        layout.addWidget(cannonball_mass_label)

        cannonball_mass_row = QHBoxLayout()
        cannonball_mass_row.addWidget(self.cannonball_mass_slider)
        cannonball_mass_row.addWidget(self.cannonball_mass_input)

        layout.addLayout(cannonball_mass_row)

        layout.addWidget(cannon_height_label)

        cannon_height_row = QHBoxLayout()
        cannon_height_row.addWidget(self.cannon_height_slider)
        cannon_height_row.addWidget(self.cannon_height_input)

        layout.addLayout(cannon_height_row)

        layout.addWidget(cannonball_radius_label)

        cannonball_radius_row = QHBoxLayout()
        cannonball_radius_row.addWidget(self.cannonball_radius_slider)
        cannonball_radius_row.addWidget(self.cannonball_radius_input)

        layout.addLayout(cannonball_radius_row)

        layout.addWidget(firing_angle_label)

        firing_angle_row = QHBoxLayout()
        firing_angle_row.addWidget(self.firing_angle_slider)
        firing_angle_row.addWidget(self.firing_angle_input)

        layout.addLayout(firing_angle_row)

        self.setLayout(layout)

    def update_initial_velocity(self, value):
        initial_velocity = value / 1000
        self.initial_velocity_input.setText(f"{initial_velocity:.3f}")
        self.main_window.change_initial_velocity_size(initial_velocity)

    def change_initial_velocity(self):
        try:
            value = float(self.initial_velocity_input.text())
            slider_value = int(value * 1000)
            self.initial_velocity_slider.setValue(slider_value)
        except ValueError:
            pass

    def update_cannonball_mass(self, value):
        cannonball_mass = value / 1000
        self.cannonball_mass_input.setText(f"{cannonball_mass:.3f}")
        self.main_window.change_cannonball_mass_size(cannonball_mass)

    def change_cannonball_mass(self):
        try:
            value = float(self.cannonball_mass_input.text())
            slider_value = int(value * 1000)
            self.cannonball_mass_slider.setValue(slider_value)
        except ValueError:
            pass

    def update_cannon_height(self, value):
        cannon_height = value / 1000
        self.cannon_height_input.setText(f"{cannon_height:.3f}")
        self.main_window.change_cannon_height_size(cannon_height)

    def change_cannon_height(self):
        try:
            value = float(self.cannon_height_input.text())
            slider_value = int(value * 1000)
            self.cannon_height_slider.setValue(slider_value)
        except ValueError:
            pass

    def update_cannonball_radius(self, value):
        cannonball_radius = value / 1000
        self.cannonball_radius_input.setText(f"{cannonball_radius:.3f}")
        self.main_window.change_cannonball_radius_size(cannonball_radius)

    def change_cannonball_radius(self):
        try:
            value = float(self.cannonball_radius_input.text())
            slider_value = int(value * 1000)
            self.cannonball_radius_slider.setValue(slider_value)
        except ValueError:
            pass

    def update_firing_angle(self, value):
        firing_angle = value / 1000
        self.firing_angle_input.setText(f"{firing_angle:.3f}")
        self.main_window.change_firing_angle_size(firing_angle)

    def change_firing_angle(self):
        try:
            value = float(self.firing_angle_input.text())
            slider_value = int(value * 1000)
            self.firing_angle_slider.setValue(slider_value)
        except ValueError:
            pass
