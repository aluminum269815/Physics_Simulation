from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class CannonballDetails(QWidget):

    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setWindowTitle("Cannonball Details")
        self.setFixedSize(350, 250)

        initial_velocity_label = QLabel("Initial Velocity")

        self.initial_velocity_slider = QSlider(Qt.Horizontal)
        self.initial_velocity_slider.setMinimum(0)
        self.initial_velocity_slider.setMaximum(100000)
        self.inital_velocity_slider.setValue(0)

        self.initial_velocity_input = QLineEdit()
        self.initial_velocity_input.setText("0")
        self.initial_velocity_input.setFixedWidth(60)

        cannonball_mass = QLabel("Cannonball Mass")

        self.cannonball_mass_slider = QSlider(Qt.Horizontal)
        self.cannonball_mass_slider.setMinimum(0)
        self.cannonball_mass_slider.setMaximum(100000)
        self.cannonball_mass_slider.setValue(0)

        self.cannonball_mass_input = QLineEdit()
        self.cannonball_mass_input.setText("0")
        self.cannonball_mass_input.setFixedWidth(60)

        cannon_height = QLabel("Cannon Height")

        self.cannon_height_slider = QSlider(Qt.Horizontal)
        self.cannon_height_slider.setMinimum(0)
        self.cannon_height_slider.setMaximum(100000)
        self.cannon_height_slider.setValue(0)

        self.cannon_height_input = QLineEdit()
        self.cannon_height_input.setText("0")
        self.cannon_height_input.setFixedWidth(60)

        cannonball_radius = QLabel("Cannon Radius")

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

        layout = QVBoxLayout()