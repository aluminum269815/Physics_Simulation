import sys
from PyQt5.QtWidgets import QWidget, QPushButton, QFrame, QVBoxLayout, QApplication
from PyQt5.QtGui import QPainter, QColor, QPolygon, QPen, QTransform
from PyQt5.QtCore import Qt, QTimer, QPoint

from settings import Settings
from constants import *
from functions import load_image
from target import Target, TargetLabel
from setting_windows import BasicParameters, VisualDisplay, CannonSettings, CannonballDetails
from cannon import CannonPlatform, CannonBase, CannonBarrel
from cannonball import CannonBall
from buttons import FireButton, PauseButton, ResetButton
from timeline import Timeline
from velocity_slider import VelocitySlider


class Program(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Projectile Motion sim")
        self.background_image = load_image('background.png')
        self.wall_image = load_image('wall.png')
        self.velocity_arrow = load_image('velocity_arrow.png')
        self.acceleration_arrow = load_image('acceleration_arrow.png')

        self.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.setStyleSheet("""
            QLabel{
                font-family: Arial;
            }
        """)

        self.settings = Settings()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(int(FRAME_INTERVAL * 1000))

        self.setting_windows = {'Basic Parameters': BasicParameters(self), 'Visual Display': VisualDisplay(self),
                                'Cannon Settings': CannonSettings(self), 'Cannonball Details': CannonballDetails(self)}

        self.cannon_platform = CannonPlatform(self)
        self.cannon_base = CannonBase(self)
        self.cannon_barrel = CannonBarrel(self)

        self.target = Target(self)
        self.target_position_label = TargetLabel(self)

        self.fire_button = FireButton(self)
        self.fire_button.move(FIRE_BUTTON_X, GROUND_Y + BUTTON_DEPTH)
        self.fire_button.clicked.connect(self.fire_cannon)

        self.pause_button = PauseButton(self)
        self.pause_button.move(PAUSE_BUTTON_X, GROUND_Y + BUTTON_DEPTH)
        self.pause_button.clicked.connect(self.switch_paused)

        self.reset_button = ResetButton(self)
        self.reset_button.move(RESET_BUTTON_X, GROUND_Y + BUTTON_DEPTH)
        self.reset_button.clicked.connect(self.reset)

        self.timeline = Timeline(self)
        self.timeline.move(900, GROUND_Y + BUTTON_DEPTH)

        self.velocity_slider = VelocitySlider(self)
        self.velocity_slider.move(50, 200)

        self.cannonballs = []
        self.selecting_cannonball = None

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

        for name in ('Basic Parameters', 'Visual Display', 'Cannon Settings', 'Cannonball Details'):
            button = QPushButton(name)
            button.clicked.connect(lambda checked, target = name: self.show_window(target))
            settings_layout.addWidget(button)

        self.settings_menu.setLayout(settings_layout)
        self.settings_menu.setVisible(False)

        settings_container_layout = QVBoxLayout()
        settings_container_layout.setContentsMargins(0, 15, 20, 0)
        settings_container_layout.setSpacing(5)
        settings_container_layout.setAlignment(Qt.AlignTop | Qt.AlignRight)

        settings_container_layout.addWidget(self.settings_panel)
        settings_container_layout.addWidget(self.settings_menu)

        self.setLayout(settings_container_layout)

    def update_frame(self):
        if not self.settings.paused and self.settings.time < self.settings.max_time:
            self.settings.time = round(self.settings.time + FRAME_INTERVAL, 3)
            self.update_cannonballs()
            self.timeline.update()
            self.setting_windows['Cannonball Details'].update_information()

    def update_cannonballs(self):
        for cannonball in self.cannonballs:
            cannonball.update()

    def change_selecting_cannonball(self, cannonball):
        self.selecting_cannonball = cannonball
        self.setting_windows['Cannonball Details'].update_information()

    def change_time(self, time):
        self.settings.set_time(time)
        self.update_cannonballs()
        self.timeline.update()
        self.setting_windows['Cannonball Details'].update_information()

    def change_cannon_height(self, height):
        self.settings.set_cannon_height(height)
        self.cannon_platform.update_position()
        self.cannon_base.update_position()
        self.cannon_barrel.update_position()
        self.setting_windows['Cannon Settings'].update_cannon_height()

    def change_dragging_firing_angle(self, firing_angle):
        self.settings.set_firing_angle(firing_angle)
        self.cannon_barrel.update_angle()
        self.cannon_barrel.update_position()
        self.setting_windows['Cannon Settings'].update_firing_angle()

    def change_firing_angle(self, firing_angle):
        self.settings.set_firing_angle(firing_angle)
        self.cannon_barrel.update_angle()
        self.cannon_platform.update_position()
        self.cannon_base.update_position()
        self.cannon_barrel.update_position()
        self.setting_windows['Cannon Settings'].update_firing_angle()

    def change_initial_velocity(self, velocity):
        self.settings.set_initial_velocity(velocity)
        self.velocity_slider.update_value()
        self.setting_windows['Cannon Settings'].update_initial_velocity()

    def toggle_settings(self):
        is_visible = self.settings_menu.isVisible()
        self.settings_menu.setVisible(not is_visible)

        if is_visible:
            self.settings_panel.setText("   Settings    ▶")
        else:
            self.settings_panel.setText("   Settings    ▼")

    def show_window(self, name):
        if self.setting_windows[name].isVisible():
            self.setting_windows[name].raise_()
            self.setting_windows[name].activateWindow()
        else:
            self.setting_windows[name].show()

    def fire_cannon(self):
        cannonball = CannonBall(self)
        self.cannonballs.append(cannonball)
        self.change_selecting_cannonball(cannonball)
        self.update_max_time()

    def reset(self):
        for cannon in self.cannonballs:
            cannon.deleteLater()
        self.cannonballs.clear()
        self.selecting_cannonball = None
        self.update_max_time()

    def update_max_time(self):
        if len(self.cannonballs) > 0:
            self.settings.set_max_time(max([cannonball.firing_time + cannonball.max_time for cannonball in self.cannonballs]))
        else:
            self.settings.set_max_time(0)
        self.timeline.update()

    def switch_paused(self):
        if self.settings.paused:
            self.play()
        else:
            self.pause()

    def play(self):
        self.settings.paused = False
        self.pause_button.set_image('playing')

    def pause(self):
        self.settings.paused = True
        self.pause_button.set_image('paused')

    def paintEvent(self, event, **kwargs):
        self.update()
        painter = QPainter(self)
        wall = self.wall_image.scaled(WALL_WIDTH, WINDOW_HEIGHT, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
        background = self.background_image.scaled(WINDOW_WIDTH - WALL_WIDTH, WINDOW_HEIGHT - GROUND_HEIGHT, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
        painter.drawPixmap(0, 0, wall)
        painter.drawPixmap(WALL_WIDTH, 0, background)
        painter.fillRect(WALL_WIDTH + CANNON_WIDTH + 50, GROUND_Y, WINDOW_WIDTH, GROUND_HEIGHT, QColor(*GROUND_COLOR))

        for cannonball in self.cannonballs:
            if self.settings.showing_trajectory:
                positions = [(cannonball.data_lists['x'][time], cannonball.data_lists['y'][time]) for time in
                             range(0, cannonball.time_index + 1, 5)]
                positions.append((cannonball.data_lists['x'][cannonball.time_index], cannonball.data_lists['y'][cannonball.time_index]))
                points = QPolygon([QPoint(int(position[0] * PIXELS_PER_METRE + WALL_WIDTH + CANNON_WIDTH),
                                          int(GROUND_Y - position[1] * PIXELS_PER_METRE)) for position in positions])
                painter.setRenderHint(QPainter.Antialiasing)
                painter.setPen(QPen(Qt.red if cannonball.air_resistance_enabled else Qt.blue, 3))
                painter.drawPolyline(points)

            if self.settings.showing_velocity_arrows:
                horizontal_velocity_arrow = self.velocity_arrow.scaled(int(80 * cannonball.current_horizontal_velocity / VELOCITY_ARROW_SCALE), 11)
                painter.drawPixmap(int(cannonball.x() + cannonball.width() / 2),
                                   int(cannonball.y() + cannonball.height() / 2 - 5),
                                       horizontal_velocity_arrow)

                vertical_velocity_arrow = self.velocity_arrow.scaled(int(80 * abs(cannonball.current_vertical_velocity) / VELOCITY_ARROW_SCALE), 11)
                transform = QTransform()
                transform.rotate(-90 if cannonball.current_vertical_velocity > 0 else 90)
                vertical_velocity_arrow = vertical_velocity_arrow.transformed(transform, Qt.SmoothTransformation)
                painter.drawPixmap(int(cannonball.x() + cannonball.width() / 2 - 5),
                                   int(cannonball.y() + cannonball.height() / 2 \
                                    - (vertical_velocity_arrow.height() if cannonball.current_vertical_velocity > 0 else 0)),
                                   vertical_velocity_arrow)

                total_velocity_arrow = self.velocity_arrow.scaled(int(80 * abs(cannonball.current_total_velocity) / VELOCITY_ARROW_SCALE), 11)
                transform = QTransform()
                transform.rotate(int(-cannonball.current_moving_direction))
                total_velocity_arrow = total_velocity_arrow.transformed(transform, Qt.SmoothTransformation)
                painter.drawPixmap(int(cannonball.x() + cannonball.width() / 2),
                                   int(cannonball.y() + cannonball.height() / 2 \
                                    - (total_velocity_arrow.height() if cannonball.current_vertical_velocity > 0 else 0)),
                                   total_velocity_arrow)

            if self.settings.showing_acceleration_arrows:
                horizontal_acceleration_arrow = self.acceleration_arrow.scaled(int(80 * abs(cannonball.current_horizontal_acceleration) / ACCELERATION_ARROW_SCALE), 11)
                transform = QTransform()
                transform.rotate(180)
                horizontal_acceleration_arrow = horizontal_acceleration_arrow.transformed(transform, Qt.SmoothTransformation)
                painter.drawPixmap(int(cannonball.x() + cannonball.width() / 2 - horizontal_acceleration_arrow.width()),
                                   int(cannonball.y() + cannonball.height() / 2 - 5),
                                       horizontal_acceleration_arrow)

                vertical_acceleration_arrow = self.acceleration_arrow.scaled(int(80 * abs(cannonball.current_vertical_acceleration) / ACCELERATION_ARROW_SCALE), 11)
                transform = QTransform()
                transform.rotate(-90 if cannonball.current_vertical_acceleration > 0 else 90)
                vertical_acceleration_arrow = vertical_acceleration_arrow.transformed(transform, Qt.SmoothTransformation)
                painter.drawPixmap(int(cannonball.x() + cannonball.width() / 2 - 5),
                                   int(cannonball.y() + cannonball.height() / 2 \
                                    - (vertical_acceleration_arrow.height() if cannonball.current_vertical_acceleration > 0 else 0)),
                                   vertical_acceleration_arrow)

                total_acceleration_arrow = self.acceleration_arrow.scaled(int(80 * abs(cannonball.current_total_acceleration) / ACCELERATION_ARROW_SCALE), 11)
                transform = QTransform()
                transform.rotate(int(-cannonball.current_accelerating_direction))
                total_acceleration_arrow = total_acceleration_arrow.transformed(transform, Qt.SmoothTransformation)
                painter.drawPixmap(int(cannonball.x() + cannonball.width() / 2 - total_acceleration_arrow.width()),
                                   int(cannonball.y() + cannonball.height() / 2),
                                   total_acceleration_arrow)



        painter.end()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Program()
    window.show()
    sys.exit(app.exec_())
