import sys
from PyQt5.QtWidgets import QWidget, QPushButton, QFrame, QVBoxLayout, QGridLayout, QApplication, QLabel, QLineEdit
from PyQt5.QtGui import QPainter, QColor, QPolygon, QPen, QBrush, QTransform, QLinearGradient
from PyQt5.QtCore import Qt, QTimer, QPoint

from settings import Settings
from constants import *
from functions import load_image
from target import Target, TargetLabel
from setting_windows import BasicParameters, VisualDisplay, CannonSettings, CannonballDetails
from cannon import CannonPlatform, CannonBase, CannonBarrel
from cannonball import CannonBall
from buttons import FireButton, ResetButton, SpeedButton, PauseButton, DeleteButton, SelectPreviousButton, SelectNextButton
from timeline import Timeline
from time_input import TimeInput
from velocity_slider import VelocitySlider


class Program(QWidget):
    def __init__(self, application):
        super().__init__()
        self.application = application
        self.setWindowTitle("Projectile Motion Simulation")
        self.background_image = load_image('background.png')
        self.wall_image = load_image('wall.png')
        self.velocity_arrow = load_image('velocity_arrow.png')
        self.acceleration_arrow = load_image('acceleration_arrow.png')


        self.setFixedSize(self.application.primaryScreen().availableGeometry().width(), self.application.primaryScreen().availableGeometry().height())
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
        self.fire_button.move(FIRE_BUTTON_X, self.height() - GROUND_HEIGHT)
        self.fire_button.clicked.connect(self.fire_cannon)

        self.controlling_frame = QFrame(self)
        self.controlling_frame.move(CONTROLLING_FRAME_X, self.height() - GROUND_HEIGHT)

        controlling_layout = QGridLayout()
        controlling_layout.setContentsMargins(75, 30, 0, 0)
        controlling_layout.setHorizontalSpacing(40)
        controlling_layout.setVerticalSpacing(40)

        self.reset_button = ResetButton(self)
        self.reset_button.clicked.connect(self.reset)
        controlling_layout.addWidget(self.reset_button, 0, 0)

        self.speed_button = SpeedButton(self)
        self.speed_button.clicked.connect(self.switch_playing_speed)
        controlling_layout.addWidget(self.speed_button, 0, 1)

        self.pause_button = PauseButton(self)
        self.pause_button.clicked.connect(self.switch_paused)
        controlling_layout.addWidget(self.pause_button, 0, 2)

        self.timeline = Timeline(self)
        controlling_layout.addWidget(self.timeline, 0, 3, Qt.AlignHCenter)
        controlling_layout.setColumnMinimumWidth(3, 1000)

        self.time_input = TimeInput(self)
        controlling_layout.addWidget(self.time_input, 0, 4)

        self.delete_button = DeleteButton(self)
        self.delete_button.clicked.connect(self.delete_cannonball)
        self.delete_button.setEnabled(False)
        controlling_layout.addWidget(self.delete_button, 1, 0)

        self.select_previous_button = SelectPreviousButton(self)
        self.select_previous_button.clicked.connect(lambda: self.select_offset_cannonball(-1))
        self.select_previous_button.setEnabled(False)
        controlling_layout.addWidget(self.select_previous_button, 1, 1)

        self.select_next_button = SelectNextButton(self)
        self.select_next_button.clicked.connect(lambda: self.select_offset_cannonball(1))
        self.select_next_button.setEnabled(False)
        controlling_layout.addWidget(self.select_next_button, 1, 2)

        self.selection_label = QLabel(self)
        self.selection_label.setText('There is no cannonball.')
        self.selection_label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.selection_label.setFixedSize(600, 80)
        self.selection_label.setStyleSheet('font-size: 30px;'
                                           'background-color: white;'
                                           'align-items: center')
        controlling_layout.addWidget(self.selection_label, 1, 3, Qt.AlignHCenter | Qt.AlignVCenter)

        self.controlling_frame.setLayout(controlling_layout)


        self.velocity_slider = VelocitySlider(self)
        self.velocity_slider.move(40, 150)

        self.cannonballs = []
        self.selecting_cannonball = None

        self.settings_menu = QFrame(self)
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
        settings_layout.setSpacing(5)

        for name in ('Basic Parameters', 'Visual Display', 'Cannon Settings', 'Cannonball Details'):
            button = QPushButton(name)
            button.clicked.connect(lambda checked, target = name: self.show_window(target))
            settings_layout.addWidget(button)

        self.settings_menu.setLayout(settings_layout)
        self.settings_menu.move(self.width() - self.settings_menu.width() - 150, 50)

    def update_frame(self):
        if not self.settings.paused and self.settings.time < self.settings.max_time:
            self.settings.time = round(self.settings.time + FRAME_INTERVAL * self.settings.playing_speed, 4)
            self.update_cannonballs()
            self.timeline.update_value()
            self.time_input.update_value()
            self.setting_windows['Cannonball Details'].update_information()

    def update_cannonballs(self):
        for cannonball in self.cannonballs:
            cannonball.update()

    def deselect_cannonball(self):
        if self.selecting_cannonball:
            self.selecting_cannonball.deselect()
            self.selecting_cannonball = None
            self.delete_button.setEnabled(False)
            self.setting_windows['Cannonball Details'].update_information()
            self.selection_label.setText(f'{len(self.cannonballs)} cannonball(s) in total.' if len(self.cannonballs) > 0 else 'There is no cannonball.')

    def change_selecting_cannonball(self, cannonball):
        self.deselect_cannonball()
        cannonball.select()
        self.selecting_cannonball = cannonball
        self.delete_button.setEnabled(True)
        self.setting_windows['Cannonball Details'].update_information()
        self.selection_label.setText(f'Selected {self.cannonballs.index(self.selecting_cannonball) + 1} of {len(self.cannonballs)} cannonball(s).')

    def change_time(self, time):
        self.settings.set_time(time)
        self.update_cannonballs()
        self.timeline.update_value()
        self.time_input.update_value()
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
        if len(self.cannonballs) >= 2:
            self.select_next_button.setEnabled(True)
            self.select_previous_button.setEnabled(True)

    def reset(self):
        self.clear()
        self.settings.reset()
        self.timeline.update_value()
        self.time_input.update_value()
        self.velocity_slider.update_value()
        self.cannon_platform.update_position()
        self.cannon_base.update_position()
        self.cannon_barrel.update_position()
        self.cannon_barrel.update_angle()
        for setting_window in self.setting_windows.values():
            setting_window.update_information()

    def clear(self):
        self.deselect_cannonball()
        for cannonball in self.cannonballs:
            cannonball.deleteLater()
        self.cannonballs.clear()
        self.update_max_time()
        self.select_previous_button.setEnabled(False)
        self.select_next_button.setEnabled(False)
        self.selection_label.setText('There is no cannonball.')

    def update_min_time(self):
        if len(self.cannonballs) > 0:
            min_time = min([cannonball.firing_time for cannonball in self.cannonballs])
            if min_time > 0:
                for cannonball in self.cannonballs:
                    cannonball.firing_time = round(cannonball.firing_time - min_time, 3)
                self.settings.set_time(round(self.settings.time - min_time, 3))

    def update_max_time(self):
        if len(self.cannonballs) > 0:
            self.settings.set_max_time(max([cannonball.firing_time + cannonball.max_time for cannonball in self.cannonballs]))
        else:
            self.settings.set_max_time(0)
        self.timeline.update_value()
        self.time_input.update_value()

    def switch_playing_speed(self):
        match self.settings.playing_speed:
            case 1.0:
                self.settings.playing_speed = 2.0
                self.speed_button.set_image('double')
            case 2.0:
                self.settings.playing_speed = 0.5
                self.speed_button.set_image('half')
            case 0.5:
                self.settings.playing_speed = 1.0
                self.speed_button.set_image('normal')

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

    def delete_cannonball(self):
        deleting_cannonball = self.selecting_cannonball
        self.cannonballs.remove(deleting_cannonball)
        self.deselect_cannonball()
        deleting_cannonball.deleteLater()
        self.update_min_time()
        self.update_max_time()
        self.setting_windows['Cannonball Details'].update_information()
        if len(self.cannonballs) > 0:
            self.select_offset_cannonball(-1)
        if len(self.cannonballs) < 2:
            self.select_next_button.setEnabled(False)
            self.select_previous_button.setEnabled(False)

    def select_offset_cannonball(self, offset):
        if self.selecting_cannonball:
            index = self.cannonballs.index(self.selecting_cannonball)
        else:
            index = 0

        index = (index + offset) % len(self.cannonballs)
        self.change_selecting_cannonball(self.cannonballs[index])

    def paintEvent(self, event, **kwargs):
        self.update()
        painter = QPainter(self)
        wall = self.wall_image.scaled(WALL_WIDTH, self.height(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
        background = self.background_image.scaled(self.width() - WALL_WIDTH, self.height() - GROUND_HEIGHT, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
        painter.drawPixmap(0, 0, wall)
        painter.drawPixmap(WALL_WIDTH, 0, background)

        vertical_shaft_gradient = QLinearGradient(WALL_WIDTH, self.height() - GROUND_HEIGHT, WALL_WIDTH + CANNON_WIDTH + 50, self.height() - GROUND_HEIGHT)
        vertical_shaft_gradient.setColorAt(0.0, QColor(*VERTICAL_SHAFT_EDGE_COLOR))
        vertical_shaft_gradient.setColorAt(0.5, QColor(*VERTICAL_SHAFT_MIDDLE_COLOR))
        vertical_shaft_gradient.setColorAt(1.0, QColor(*VERTICAL_SHAFT_EDGE_COLOR))
        vertical_shaft_brush = QBrush(vertical_shaft_gradient)
        painter.fillRect(WALL_WIDTH, self.height() - GROUND_HEIGHT, CANNON_WIDTH + 50, GROUND_HEIGHT, vertical_shaft_brush)

        ground_gradient = QLinearGradient(0, self.height() - GROUND_HEIGHT, 0, self.height())
        ground_gradient.setColorAt(0.0, QColor(*GROUND_TOP_COLOR))
        ground_gradient.setColorAt(1.0, QColor(*GROUND_BOTTOM_COLOR))
        ground_brush = QBrush(ground_gradient)
        painter.fillRect(WALL_WIDTH + CANNON_WIDTH + 50, self.height() - GROUND_HEIGHT, self.width(), GROUND_HEIGHT, ground_brush)

        for cannonball in self.cannonballs:
            if self.settings.showing_trajectory:
                positions = [(cannonball.data_lists['x'][time], cannonball.data_lists['y'][time]) for time in
                             range(0, cannonball.time_index + 1, 5)]
                positions.append((cannonball.data_lists['x'][cannonball.time_index], cannonball.data_lists['y'][cannonball.time_index]))
                points = QPolygon([QPoint(int(position[0] * PIXELS_PER_METRE + WALL_WIDTH + CANNON_WIDTH),
                                          int(self.height() - GROUND_HEIGHT - position[1] * PIXELS_PER_METRE)) for position in positions])
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

                if cannonball.air_resistance_enabled:
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
    window = Program(app)
    window.showMaximized()
    sys.exit(app.exec_())
