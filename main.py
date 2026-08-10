import os, sys

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from settings import Settings
from basicparameters import BasicParameters
from visualdisplay import VisualDisplay
from cannonsettings import CannonSettings
from cannonballdetails import CannonballDetails
import equations
from target import Target


class Program(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Projectile Motion sim")
        self.background = QPixmap(os.path.abspath("asset/background.png"))
        self.resize(1100, 650)
        self.setStyleSheet("""
            QLabel{
                font-family: Arial;
            }
        """)

        self.basic_parameters_window = None
        self.visual_display_window = None
        self.cannon_settings_window = None
        self.cannonball_details_window = None

        self.air_density = 1.225
        self.gravity = 9.81
        self.initial_velocity = 30.0
        self.cannonball_mass = 10.0
        self.cannon_height = 0.0
        self.cannonball_radius = 20.0
        self.firing_angle = 45.0
        self.time = 0.0

        self.v_horizontal = 0.0
        self.v_vertical = 0.0
        self.v_total = 0.0
        self.a_horizontal = 0.0
        self.a_vertical = 0.0
        self.a_total = 0.0
        self.kinetic_energy = 0.0
        self.gpe = 0.0
        self.position_horizontal = 0.0
        self.position_vertical = 0.0

        self.recalculate()

        self.pixels_per_meter = 20
        self.origin_x = 100
        self.origin_y = int(self.height() * 0.88)

        self.target = Target(self)
        self.target.ground_y = self.origin_y
        self.target.moveTo(500, self.target.ground_y - self.target.height())
        self.target.moved.connect(self.update_target_position_label)

        self.target_position_label = QLabel(self)
        self.target_position_label.setStyleSheet("""
            background-color: rgba(255, 255, 255, 190);
            padding: 2px 6px;
            border-radius: 4px;
            font-family: Arial;
            font-size: 11px;
        """)
        self.update_target_position_label(self.target.x(), self.target.y())

        self.settings = Settings()

        self.settings_panel = QPushButton("⚙ Settings    ▼")
        self.settings_panel.clicked.connect(self.toggle_settings)
        self.settings_panel.setFixedSize(150, 40)

        self.settings_menu = QFrame()

        self.settings_menu.setStyleSheet("""
            QFrame {
                background-color: #c2c1c2;
                border: 1px solid #cccccc;
                border-radius: 8px;
            }

            QPushButton {
                background-color: #c2c1c2;
                color: black;
                border: grey;
                padding: 8px;
                text-align: left;
                border-radius: 4px;
                font-family: Arial;
            }

            QPushButton:hover {
                background-color: #eeeeee;
                font-family: Arial;
                font-weight: bold;
            }
        """)

        settings_layout = QVBoxLayout()

        settings_layout.setContentsMargins(8, 8, 8, 8)
        settings_layout.setSpacing(4)

        self.settings_menu.setLayout(settings_layout)

        self.basic_parameters_button = QPushButton("Basic Parameters")
        self.visual_display_button = QPushButton("Visual Displays")
        self.cannon_settings_button = QPushButton("Cannon Settings")
        self.cannonball_details_button = QPushButton("Cannonball Details")

        settings_layout.addWidget(self.basic_parameters_button)
        settings_layout.addWidget(self.visual_display_button)
        settings_layout.addWidget(self.cannon_settings_button)
        settings_layout.addWidget(self.cannonball_details_button)

        self.basic_parameters_button.clicked.connect(self.unfold_basic_parameters)
        self.visual_display_button.clicked.connect(self.unfold_visual_display)
        self.cannon_settings_button.clicked.connect(self.unfold_cannon_settings)
        self.cannonball_details_button.clicked.connect(self.unfold_cannonball_details)

        self.settings_menu.setVisible(False)

        self.settings_container = QWidget()

        settings_container_layout = QVBoxLayout()

        settings_container_layout.setContentsMargins(0, 15, 20, 0)
        settings_container_layout.setSpacing(5)
        settings_container_layout.setAlignment(Qt.AlignTop | Qt.AlignRight)

        settings_container_layout.addWidget(self.settings_panel)
        settings_container_layout.addWidget(self.settings_menu)

        self.settings_container.setLayout(settings_container_layout)

        layout = QVBoxLayout()

        layout.setContentsMargins(0, 0, 0, 0)

        layout.addWidget(self.settings_container)

        layout.addStretch()

        layout.addStretch()

        self.setLayout(layout)

    def toggle_settings(self):
        is_visible = self.settings_menu.isVisible()

        self.settings_menu.setVisible(not is_visible)

        if is_visible:
            self.settings_panel.setText("⚙ Settings    ▶")
        else:
            self.settings_panel.setText("⚙ Settings    ▼")

    def unfold_basic_parameters(self):
        if self.basic_parameters_window is not None and self.basic_parameters_window.isVisible():
            self.basic_parameters_window.raise_()
            self.basic_parameters_window.activateWindow()
            return
        self.basic_parameters_window = BasicParameters(self)
        self.basic_parameters_window.show()

    def unfold_visual_display(self):
        if self.visual_display_window is not None and self.visual_display_window.isVisible():
            self.visual_display_window.raise_()
            self.visual_display_window.activateWindow()
            return
        self.visual_display_window = VisualDisplay(self)
        self.visual_display_window.show()

    def unfold_cannon_settings(self):
        if self.cannon_settings_window is not None and self.cannon_settings_window.isVisible():
            self.cannon_settings_window.raise_()
            self.cannon_settings_window.activateWindow()
            return
        self.cannon_settings_window = CannonSettings(self)
        self.cannon_settings_window.show()

    def unfold_cannonball_details(self):
        if self.cannonball_details_window is not None and self.cannonball_details_window.isVisible():
            self.cannonball_details_window.raise_()
            self.cannonball_details_window.activateWindow()
            return
        self.cannonball_details_window = CannonballDetails(self)
        self.cannonball_details_window.update_display()
        self.cannonball_details_window.show()

    def change_air_density_size(self, value):
        self.air_density = value
        self.recalculate()
        self.update_cannonball_details_display()

    def change_gravity_size(self, value):
        self.gravity = value
        self.recalculate()
        self.update_cannonball_details_display()

    def change_initial_velocity_size(self, value):
        self.initial_velocity = value
        self.recalculate()
        self.update_cannonball_details_display()

    def change_cannonball_mass_size(self, value):
        self.cannonball_mass = value
        self.recalculate()
        self.update_cannonball_details_display()

    def change_cannon_height_size(self, value):
        self.cannon_height = value
        self.recalculate()
        self.update_cannonball_details_display()

    def change_cannonball_radius_size(self, value):
        self.cannonball_radius = value
        self.update_cannonball_details_display()

    def change_firing_angle_size(self, value):
        self.firing_angle = value
        self.recalculate()
        self.update_cannonball_details_display()

    def recalculate(self):
        self.v_horizontal, self.v_vertical = equations.velocity_components(self.initial_velocity, self.firing_angle,
                                                                           self.time, self.gravity)
        self.v_total = equations.total_velocity(self.v_horizontal, self.v_vertical)

        self.a_horizontal, self.a_vertical = equations.acceleration_components(self.gravity)
        self.a_total = equations.total_acceleration(self.a_horizontal, self.a_vertical)

        self.kinetic_energy = equations.ke(self.cannonball_mass, self.v_total)
        self.gpe = equations.gpe(self.cannonball_mass, self.gravity, self.cannon_height)

        self.position_horizontal, self.position_vertical = equations.position(self.initial_velocity, self.firing_angle,
                                                                              self.time, self.gravity,
                                                                              self.cannon_height)

    def update_cannonball_details_display(self):
        if self.cannonball_details_window is not None:
            self.cannonball_details_window.update_display()

    def pixels_to_metres(self, px, py):
        centre_x = px + (self.target.width() / 2)
        bottom_y = py + self.target.height()

        x_metres = (centre_x - self.origin_x) / self.pixels_per_meter
        y_metres = (self.origin_y - bottom_y) / self.pixels_per_meter

        return x_metres, y_metres

    def update_target_position_label(self, px, py):
        x_metres, y_metres = self.pixels_to_metres(px, py)
        self.target_position_label.setText(f"{x_metres:.2f} m, {y_metres:.2f} m")
        self.target_position_label.adjustSize()

        label_x = px + (self.target.width() // 2) - (self.target_position_label.width() // 2)
        label_y = py - self.target_position_label.height() - 4
        self.target_position_label.move(label_x, label_y)

    def paintEvent(self, event):
        painter = QPainter(self)
        scaled = self.background.scaled(self.size(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
        painter.drawPixmap(0, 0, scaled)

    def resizeEvent(self, event):
        self.origin_y = int(self.height() * 0.88)
        self.target.ground_y = self.origin_y
        max_y = self.target.ground_y - self.target.height()
        if self.target.y() > max_y:
            self.target.moveTo(self.target.x(), max_y)
        else:
            self.update_target_position_label(self.target.x(), self.target.y())
        super().resizeEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Program()
    window.show()
    sys.exit(app.exec_())

