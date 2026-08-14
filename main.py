import os, sys
import math

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
from cannon import Cannon
from buttons import FireButton
from cannonballflying import CannonballFlight, CannonballPreview, VectorArrow
from timeline import PauseResumeButton

VELOCITY_ARROW_SCALE = 3
ACCELERATION_ARROW_SCALE = 3


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
        self.air_resistance_enabled = False
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

        self.show_velocity_arrows = False
        self.show_acceleration_arrows = False
        self.flight_history = []
        self.flight_duration_estimate = 0.0

        self.recalculate()

        self.pixels_per_meter = 2
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

        self.wall_width_ratio = 78 / 1774

        self.cannon = Cannon(self, ground_y=self.origin_y + 0, top_y=0, lift_height = 60, head_height = 28)
        self.position_cannon_x()

        self.velocity_arrow = VectorArrow(self, QColor(220, 30, 30))
        self.acceleration_arrow = VectorArrow(self, QColor(30, 90, 220))
        self.velocity_arrow.setGeometry(0, 0, self.width(), self.height())
        self.acceleration_arrow.setGeometry(0, 0, self.width(), self.height())

        self.flying_cannonball = None
        self.fire_button = FireButton(self)
        self.fire_button.clicked.connect(self.fire_cannon)
        self.position_fire_button()

        self.cannonball_preview = CannonballPreview(self)
        self.cannonball_preview.show()

        self.pause_resume_button = PauseResumeButton(self)
        self.pause_resume_button.clicked.connect(self.toggle_pause_resume)
        self.pause_resume_button.setEnabled(False)

        self.timeline_slider = QSlider(Qt.Horizontal, self)
        self.timeline_slider.setMinimum(0)
        self.timeline_slider.setMaximum(1000)
        self.timeline_slider.setEnabled(False)
        self.timeline_slider.sliderPressed.connect(self.on_timeline_pressed)
        self.timeline_slider.valueChanged.connect(self.on_timeline_scrubbed)

        self.position_timeline()

        self.cannon.moved.connect(self.on_cannon_moved)
        self.cannon.moveTo(self.origin_y - self.cannon.lift_bottom_offset)
        self.cannon.set_firing_angle(self.firing_angle)

        self.update_cannonball_preview()

        self.settings = Settings()

        self.settings_panel = QPushButton("   Settings    ▼")
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
            self.settings_panel.setText("   Settings    ▶")
        else:
            self.settings_panel.setText("   Settings    ▼")

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
        self.update_cannon_position()

    def change_air_resistance_enabled(self, enabled):
        self.air_resistance_enabled = enabled

    def change_show_velocity_arrows(self, enabled):
        self.show_velocity_arrows = enabled
        if not enabled:
            self.velocity_arrow.hide_arrow()
        elif self.flying_cannonball is not None:
            self.update_arrows(self.position_horizontal, self.position_vertical,
                                self.v_horizontal, self.v_vertical,
                                self.a_horizontal, self.a_vertical)

    def change_show_acceleration_arrows(self, enabled):
        self.show_acceleration_arrows = enabled
        if not enabled:
            self.acceleration_arrow.hide_arrow()
        elif self.flying_cannonball is not None:
            self.update_arrows(self.position_horizontal, self.position_vertical,
                                self.v_horizontal, self.v_vertical,
                                self.a_horizontal, self.a_vertical)

    def change_cannonball_radius_size(self, value):
        self.cannonball_radius = value
        self.update_cannonball_details_display()
        self.update_cannonball_preview()

    def change_firing_angle_size(self, value):
        self.firing_angle = value
        self.recalculate()
        self.update_cannonball_details_display()
        self.cannon.set_firing_angle(value)
        self.update_cannonball_preview()

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

    def position_cannon_x(self):
        wall_width = int(self.width() * self.wall_width_ratio)
        overlap = 5
        cannon_x = max(0, wall_width - overlap)
        self.cannon.move(cannon_x, self.cannon.y())

    def position_fire_button(self):
        x = self.cannon.x()
        y = self.origin_y + 10
        self.fire_button.move(x, y)

    def position_timeline(self):
        margin = 10
        y = self.fire_button.y()
        row_height = self.fire_button.height()

        pause_size = self.pause_resume_button.height()
        pause_x = self.fire_button.x() + self.fire_button.width() + margin
        pause_y = y + (row_height - pause_size) // 2
        self.pause_resume_button.move(pause_x, pause_y)

        slider_height = 20
        slider_x = pause_x + self.pause_resume_button.width() + margin
        slider_y = y + (row_height - slider_height) // 2
        slider_width = max(50, self.width() - slider_x - margin)
        self.timeline_slider.setGeometry(slider_x, slider_y, slider_width, slider_height)

    def update_cannonball_preview(self):
        self.cannonball_preview.set_radius(self.cannonball_radius / 100)
        self.cannonball_preview.reposition_at(self.cannon.muzzle_point())

    def fire_cannon(self):
        if self.flying_cannonball is not None:
            self.flying_cannonball.stop()
            self.flying_cannonball.deleteLater()
            self.flying_cannonball = None

        self.cannonball_preview.hide()

        muzzle_px = self.cannon.muzzle_point()
        start_x_m = (muzzle_px.x() - self.origin_x) / self.pixels_per_meter
        start_y_m = (self.origin_y - muzzle_px.y()) / self.pixels_per_meter

        angle_rad = math.radians(self.firing_angle)
        velocity_x = self.initial_velocity * math.cos(angle_rad)
        velocity_y = self.initial_velocity * math.sin(angle_rad)

        radius_m = self.cannonball_radius / 100

        self.flying_cannonball = CannonballFlight(
            self, start_x_m, start_y_m, velocity_x, velocity_y,
            self.cannonball_mass, radius_m
        )
        self.flying_cannonball.landed.connect(self.on_cannonball_landed)
        self.flying_cannonball.show()
        self.flying_cannonball.raise_()

        discriminant = (velocity_y ** 2) + (2 * self.gravity * start_y_m)
        t_estimate = (velocity_y + math.sqrt(max(discriminant, 0))) / self.gravity
        self.flight_duration_estimate = max(0.5, t_estimate * 1.2)

        self.flight_history = []
        self.timeline_slider.blockSignals(True)
        self.timeline_slider.setMaximum(1000)
        self.timeline_slider.setValue(0)
        self.timeline_slider.blockSignals(False)
        self.timeline_slider.setEnabled(True)

        self.pause_resume_button.setEnabled(True)
        self.pause_resume_button.set_playing_state(True)

        self.flying_cannonball.start()
        self.fire_button.setEnabled(False)

    def on_cannonball_physics_update(self, t, x_m, y_m, vx, vy, ax, ay):
        self.position_horizontal = x_m
        self.position_vertical = y_m
        self.v_horizontal = vx
        self.v_vertical = vy
        self.v_total = math.hypot(vx, vy)
        self.a_horizontal = ax
        self.a_vertical = ay
        self.a_total = math.hypot(ax, ay)
        self.kinetic_energy = 0.5 * self.cannonball_mass * (self.v_total ** 2)
        self.gpe = self.cannonball_mass * self.gravity * max(y_m, 0)
        self.update_cannonball_details_display()
        self.update_arrows(x_m, y_m, vx, vy, ax, ay)

        self.flight_history.append((t, x_m, y_m, vx, vy, ax, ay))
        progress = min(1000, int((t / self.flight_duration_estimate) * 1000)) if self.flight_duration_estimate > 0 else 0
        self.timeline_slider.blockSignals(True)
        self.timeline_slider.setValue(progress)
        self.timeline_slider.blockSignals(False)

    def update_arrows(self, x_m, y_m, vx, vy, ax, ay):
        centre_px_x = self.origin_x + x_m * self.pixels_per_meter
        centre_px_y = self.origin_y - y_m * self.pixels_per_meter
        start = QPointF(centre_px_x, centre_px_y)

        if self.show_velocity_arrows:
            end = QPointF(centre_px_x + vx * VELOCITY_ARROW_SCALE, centre_px_y - vy * VELOCITY_ARROW_SCALE)
            self.velocity_arrow.set_vector(start, end)
            self.velocity_arrow.show_arrow()
        else:
            self.velocity_arrow.hide_arrow()

        if self.show_acceleration_arrows:
            end = QPointF(centre_px_x + ax * ACCELERATION_ARROW_SCALE, centre_px_y - ay * ACCELERATION_ARROW_SCALE)
            self.acceleration_arrow.set_vector(start, end)
            self.acceleration_arrow.show_arrow()
        else:
            self.acceleration_arrow.hide_arrow()

    def on_cannonball_landed(self):
        self.fire_button.setEnabled(True)
        self.pause_resume_button.set_playing_state(False)
        self.update_cannonball_preview()
        self.cannonball_preview.show()

        self.timeline_slider.blockSignals(True)
        self.timeline_slider.setValue(1000)
        self.timeline_slider.blockSignals(False)

    def toggle_pause_resume(self):
        if self.flying_cannonball is None:
            return
        if self.flying_cannonball.is_paused():
            current_progress = self.timeline_slider.value()
            target_t = (current_progress / 1000) * self.flight_duration_estimate if self.flight_duration_estimate > 0 else 0

            if self.flight_history:
                closest_index = min(
                    range(len(self.flight_history)),
                    key=lambda i: abs(self.flight_history[i][0] - target_t)
                )
                t, x_m, y_m, vx, vy, ax, ay = self.flight_history[closest_index]
                self.flight_history = self.flight_history[:closest_index + 1]
                self.flying_cannonball.set_full_state(x_m, y_m, vx, vy, t)

                progress = min(1000, int((t / self.flight_duration_estimate) * 1000)) if self.flight_duration_estimate > 0 else 0
                self.timeline_slider.blockSignals(True)
                self.timeline_slider.setValue(progress)
                self.timeline_slider.blockSignals(False)

            self.flying_cannonball.resume()
            self.pause_resume_button.set_playing_state(True)
        else:
            self.flying_cannonball.pause()
            self.pause_resume_button.set_playing_state(False)

    def on_timeline_pressed(self):
        if self.flying_cannonball is not None and not self.flying_cannonball.is_paused():
            self.flying_cannonball.pause()
            self.pause_resume_button.set_playing_state(False)

    def on_timeline_scrubbed(self, progress):
        if not self.flight_history or self.flight_duration_estimate <= 0:
            return

        target_t = (progress / 1000) * self.flight_duration_estimate
        t, x_m, y_m, vx, vy, ax, ay = min(self.flight_history, key=lambda entry: abs(entry[0] - target_t))

        self.position_horizontal = x_m
        self.position_vertical = y_m
        self.v_horizontal = vx
        self.v_vertical = vy
        self.v_total = math.hypot(vx, vy)
        self.a_horizontal = ax
        self.a_vertical = ay
        self.a_total = math.hypot(ax, ay)
        self.kinetic_energy = 0.5 * self.cannonball_mass * (self.v_total ** 2)
        self.gpe = self.cannonball_mass * self.gravity * max(y_m, 0)
        self.update_cannonball_details_display()
        self.update_arrows(x_m, y_m, vx, vy, ax, ay)

        if self.flying_cannonball is not None:
            self.flying_cannonball.set_state(x_m, y_m)
            self.pause_resume_button.setEnabled(True)
            self.pause_resume_button.set_playing_state(False)

    def update_cannon_position(self):
        height_pixels = int(self.cannon_height * self.pixels_per_meter)
        new_y = self.cannon.ground_y - self.cannon.lift_bottom_offset - height_pixels
        self.cannon.moveTo(new_y)
        self.update_cannonball_preview()

    def on_cannon_moved(self, y):
        height_pixels = self.cannon.ground_y - self.cannon.lift_bottom_offset - y
        height_metres = height_pixels / self.pixels_per_meter

        self.cannon_height = height_metres
        self.recalculate()
        self.update_cannonball_details_display()
        self.update_cannonball_preview()

        if self.cannon_settings_window is not None and self.cannon_settings_window.isVisible():
            self.cannon_settings_window.sync_cannon_height_display(height_metres)

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

        self.position_cannon_x()
        self.cannon.ground_y = self.origin_y + 0
        self.update_cannon_position()
        self.position_fire_button()

        if hasattr(self, "velocity_arrow"):
            self.velocity_arrow.setGeometry(0, 0, self.width(), self.height())
            self.acceleration_arrow.setGeometry(0, 0, self.width(), self.height())

        if hasattr(self, "pause_resume_button"):
            self.position_timeline()

        super().resizeEvent(event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Program()
    window.show()
    sys.exit(app.exec_())