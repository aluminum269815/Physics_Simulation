import math

from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPainter, QColor, QRadialGradient, QPen, QPolygon, QPixmap
from PyQt5.QtCore import Qt, QTimer, QPoint, pyqtSignal

from constants import *
from functions import load_image


class CannonBall(QLabel):
    def __init__(self, program):
        super().__init__(program)
        self.program = program
        self.settings = self.program.settings

        self.gravity = self.settings.gravity
        self.air_resistance_enabled = self.settings.air_resistance_enabled
        self.air_density = self.settings.air_density
        self.drag_coefficient = self.settings.drag_coefficient
        self.firing_time = self.settings.time
        
        self.time_after_firing = 0
        self.time_index = 0
        self.fired = True
        self.landed = False

        self.mass = self.settings.cannonball_mass
        self.radius = self.settings.cannonball_radius

        self.initial_height = self.settings.cannon_height
        self.initial_total_velocity = self.settings.initial_velocity
        self.initial_moving_direction = self.settings.firing_angle
        self.initial_horizontal_velocity = \
            round(self.initial_total_velocity * math.cos(math.radians(self.initial_moving_direction)), 5)
        self.initial_vertical_velocity = \
            round(self.initial_total_velocity * math.sin(math.radians(self.initial_moving_direction)), 5)

        self.initial_kinetic_energy = round(0.5 * self.mass * self.initial_total_velocity ** 2, 5)
        self.initial_gravitational_potential_energy = round(self.gravity * self.mass * self.initial_height, 5)
        self.initial_total_energy = self.initial_kinetic_energy + self.initial_gravitational_potential_energy

        self.current_distance = 0
        self.current_height = 0
        self.current_horizontal_velocity = 0
        self.current_vertical_velocity = 0
        self.current_total_velocity = 0
        self.current_moving_direction = 0

        self.current_horizontal_acceleration = 0
        self.current_vertical_acceleration = 0
        self.current_total_acceleration = 0
        self.current_accelerating_direction = 0

        self.current_kinetic_energy = 0
        self.current_gravitational_potential_energy = 0
        self.current_total_energy = 0
        self.energy_loss = 0
        
        self.data_lists = {
            'x': [0], 
            'y': [self.initial_height], 
            'xv': [self.initial_horizontal_velocity], 
            'yv': [self.initial_vertical_velocity],
            'xa': [],
            'ya': [],
            'tv': [self.initial_total_velocity],
            'ke': [round(0.5 * self.mass * self.initial_total_velocity ** 2, 5)],
            'gpe': [round(self.gravity * self.mass * self.current_height, 5)]
        }
        self.calculate_data_lists()
        self.max_time = round((len(self.data_lists['x']) - 1) * FRAME_INTERVAL, 3)


        self.default_image = None
        self.selecting_image = None
        self.create_image()
        self.update()

    def __getitem__(self, item):
        return self.data_lists[item][self.time_index]

    def calculate_data_lists(self):
        if self.air_resistance_enabled:
            drag_constant = round(0.5 * self.air_density * self.drag_coefficient * self.radius ** 2 * math.pi, 5)
            self.data_lists['xa'] = [round(- drag_constant / self.mass * self.initial_horizontal_velocity * self.initial_total_velocity, 5)]
            self.data_lists['ya'] = [round(- self.gravity - drag_constant / self.mass * self.initial_vertical_velocity * self.initial_total_velocity, 5)]

            while self.data_lists['y'][-1] > 0 or len(self.data_lists['x']) == 1:
                self.data_lists['xv'].append(
                    round(self.data_lists['xv'][-1] + FRAME_INTERVAL * self.data_lists['xa'][-1], 5))
                self.data_lists['yv'].append(
                    round(self.data_lists['yv'][-1] + FRAME_INTERVAL * self.data_lists['ya'][-1], 5))
                self.data_lists['x'].append(
                    round(self.data_lists['x'][-1] + FRAME_INTERVAL * self.data_lists['xv'][-1], 5))
                self.data_lists['y'].append(
                    round(self.data_lists['y'][-1] + FRAME_INTERVAL * self.data_lists['yv'][-1], 5))
                tv = round(math.sqrt(self.data_lists['xv'][-1] ** 2 + self.data_lists['yv'][-1] ** 2), 5)
                self.data_lists['xa'].append(
                    round(- drag_constant / self.mass * self.data_lists['xv'][-1] * tv, 5))
                self.data_lists['ya'].append(
                    round(- self.gravity - drag_constant / self.mass * self.data_lists['yv'][-1] * tv, 5))
                self.data_lists['tv'].append(round(math.sqrt(self.data_lists['xv'][-1] ** 2 \
                                                             + self.data_lists['yv'][-1] ** 2), 5))
                self.data_lists['ke'].append(round(0.5 * self.mass * self.data_lists['tv'][-1] ** 2, 5))
                self.data_lists['gpe'].append(round(self.gravity * self.mass * self.data_lists['y'][-1], 5))

        else:
            self.data_lists['xa'] = [0]
            self.data_lists['ya'] = [- self.gravity]

            while self.data_lists['y'][-1] > 0 or len(self.data_lists['x']) == 1:
                time_after_firing = len(self.data_lists['x']) * FRAME_INTERVAL
                self.data_lists['x'].append(round(self.initial_horizontal_velocity * time_after_firing, 5))
                self.data_lists['y'].append(round(self.initial_height + time_after_firing * self.initial_vertical_velocity \
                                            - self.gravity / 2 * time_after_firing ** 2, 5))
                self.data_lists['xv'].append(self.initial_horizontal_velocity)
                self.data_lists['yv'].append(round(self.initial_vertical_velocity \
                                            - self.gravity * time_after_firing, 5))
                self.data_lists['xa'].append(0)
                self.data_lists['ya'].append(- self.gravity)
                self.data_lists['tv'].append(round(math.sqrt(self.data_lists['xv'][-1] ** 2 \
                                                             + self.data_lists['yv'][-1] ** 2), 5))
                self.data_lists['ke'].append(round(0.5 * self.mass * self.data_lists['tv'][-1] ** 2, 5))
                self.data_lists['gpe'].append(round(self.gravity * self.mass * self.data_lists['y'][-1], 5))

            self.data_lists['ke'][-1] = self.initial_total_energy

        self.data_lists['y'][-1] = self.data_lists['gpe'][-1] = 0

    def create_image(self):
        diameter = max(10, min(50, int(self.radius * CANNONBALL_SCALE)))
        self.default_image = QPixmap(diameter, diameter)
        self.default_image.fill(Qt.transparent)

        painter = QPainter(self.default_image)
        painter.setRenderHint(QPainter.Antialiasing)
        gradient = QRadialGradient(diameter * 0.35, diameter * 0.35, diameter * 0.9)
        gradient.setColorAt(0, QColor(110, 110, 110))
        gradient.setColorAt(1, QColor(25, 25, 25))
        painter.setBrush(gradient)
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(0, 0, diameter, diameter)
        painter.end()

        self.selecting_image = QPixmap(diameter, diameter)
        self.selecting_image.fill(Qt.transparent)

        painter = QPainter(self.selecting_image)
        painter.setRenderHint(QPainter.Antialiasing)
        gradient = QRadialGradient(diameter * 0.35, diameter * 0.35, diameter * 0.9)
        gradient.setColorAt(0, QColor(210, 210, 110))
        gradient.setColorAt(1, QColor(125, 125, 25))
        painter.setBrush(gradient)
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(0, 0, diameter, diameter)
        painter.end()

        self.setPixmap(self.default_image)
        self.setFixedSize(self.default_image.size())

    def update(self):
        self.update_time()
        self.update_data()
        self.update_position()
    
    def update_time(self):
        self.time_after_firing = round(self.settings.time - self.firing_time, 3)
        self.time_after_firing = min(self.time_after_firing, self.max_time)
        self.fired = self.time_after_firing >= 0
        self.setVisible(self.fired)
        self.landed = self.time_after_firing == self.max_time
        self.time_after_firing = max(self.time_after_firing, 0)
        self.time_index = int(self.time_after_firing * 1000) // int(FRAME_INTERVAL * 1000)

    def update_data(self):
        self.current_distance = self.data_lists['x'][self.time_index]
        self.current_height = self.data_lists['y'][self.time_index]

        self.current_horizontal_velocity = self.data_lists['xv'][self.time_index]
        self.current_vertical_velocity = self.data_lists['yv'][self.time_index]
        self.current_total_velocity = self.data_lists['tv'][self.time_index]
        self.current_moving_direction = round(math.degrees(math.atan2(self.current_vertical_velocity,
                                                                      self.current_horizontal_velocity)), 5)

        self.current_horizontal_acceleration = self.data_lists['xa'][self.time_index]
        self.current_vertical_acceleration = self.data_lists['ya'][self.time_index]
        self.current_total_acceleration = round(math.sqrt(self.current_horizontal_acceleration ** 2 \
                                                          + self.current_vertical_acceleration ** 2), 5)
        self.current_accelerating_direction = round(math.degrees(math.atan2(self.current_vertical_acceleration,
                                                                            self.current_horizontal_acceleration)), 5)

        self.current_kinetic_energy = self.data_lists['ke'][self.time_index]
        self.current_gravitational_potential_energy = self.data_lists['gpe'][self.time_index]
        self.current_total_energy = round(self.current_kinetic_energy + self.current_gravitational_potential_energy, 2)
        self.energy_loss = round(self.initial_total_energy - self.current_total_energy, 2)

    def update_position(self):
        x = WALL_WIDTH + CANNON_WIDTH + self.current_distance * PIXELS_PER_METRE - self.width() // 2
        y = GROUND_Y - self.current_height * PIXELS_PER_METRE - self.height() // 2
        self.move(int(x), int(y))

    def mousePressEvent(self, event, **kwargs):
        if event.button() == Qt.LeftButton:
            if self is not self.program.selecting_cannonball:
                self.program.change_selecting_cannonball(self)
            else:
                self.program.deselect_cannonball()

    def select(self):
        self.setPixmap(self.selecting_image)

    def deselect(self):
        self.setPixmap(self.default_image)
