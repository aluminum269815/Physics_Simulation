import math

class CannonBall:
    def __init__(self, program):
        self.program = program
        settings = self.program.settings

        self.gravity = settings.gravity
        self.air_resistance_enabled = settings.air_resistance_enabled
        self.air_density = settings.air_density
        self.drag_coefficient = settings.drag_coefficient

        self.time_after_firing = 0

        self.mass = settings.cannonball_mass
        self.radius = settings.cannonball_radius

        self.initial_height = settings.cannon_height
        self.initial_total_velocity = settings.initial_cannon_velocity
        self.initial_moving_direction = settings.firing_angle
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
        self.current_acceleration_direction = 0

        self.current_kinetic_energy = 0
        self.current_gravitational_potential_energy = 0
        self.current_total_energy = 0
        self.energy_loss = 0

        if self.air_resistance_enabled:
            self.time_index = 0
            self.drag_constant = round(0.5 * self.air_density * self.drag_coefficient * self.radius ** 2 * math.pi, 5)
            self.data_lists = {
                'x': [0], 'y': [self.initial_height],
                'xv': [self.initial_vertical_velocity], 'yv': [self.initial_horizontal_velocity],
                'xa': [round(- self.drag_constant / self.mass \
                        * self.initial_horizontal_velocity * self.initial_total_velocity, 5)],
                'ya': [round(- self.gravity - self.drag_constant / self.mass \
                       * self.initial_vertical_velocity * self.initial_total_velocity, 5)]
            }
            self.calculate_data_lists()

        self.update_data()

    def calculate_data_lists(self):
        while self.data_lists['y'][-1] >= 0:
            self.data_lists['xv'].append(round(self.data_lists['xv'][-1] + 0.001 * self.data_lists['xa'][-1], 5))
            self.data_lists['yv'].append(round(self.data_lists['yv'][-1] + 0.001 * self.data_lists['ya'][-1], 5))
            self.data_lists['x'].append(round(self.data_lists['x'][-1] + 0.001 * self.data_lists['xv'][-1], 5))
            self.data_lists['y'].append(round(self.data_lists['y'][-1] + 0.001 * self.data_lists['yv'][-1], 5))
            tv = round(math.sqrt(self.data_lists['xv'][-1] ** 2 + self.data_lists['yv'][-1] ** 2), 5)
            self.data_lists['xa'].append(round(- self.drag_constant / self.mass * self.data_lists['xv'][-1] * tv, 5))
            self.data_lists['ya'].append(round(- self.gravity - self.drag_constant / self.mass * self.data_lists['yv'][-1] * tv, 5))
        self.data_lists['y'][-1] = 0


    def update(self):
        self.update_data()

    def update_data(self):
        if self.air_resistance_enabled:
            self.time_index = min(int(self.time_after_firing // 0.001), len(self.data_lists['height']))
        self.update_position()
        self.update_velocity()
        self.update_acceleration()
        self.update_energy()

    def update_position(self):
        if self.air_resistance_enabled:
            self.current_distance = self.data_lists['x'][self.time_index]
            self.current_height = self.data_lists['y'][self.time_index]
        else:
            self.current_distance = round(self.initial_horizontal_velocity * self.time_after_firing, 5)
            self.current_height = round(self.initial_height + self.time_after_firing * self.initial_vertical_velocity \
                                  - self.gravity / 2 * self.time_after_firing ** 2, 5)

    def update_velocity(self):
        if self.air_resistance_enabled:
            self.current_horizontal_velocity = self.data_lists['xv'][self.time_index]
            self.current_vertical_velocity = self.data_lists['yv'][self.time_index]
        else:
            self.current_horizontal_velocity = self.initial_horizontal_velocity
            self.current_vertical_velocity = round(self.initial_vertical_velocity \
                                                   - self.gravity * self.time_after_firing, 5)

        self.current_total_velocity = round(math.sqrt(self.current_horizontal_velocity ** 2 \
                                                    + self.current_vertical_velocity ** 2), 5)
        self.current_moving_direction = round(math.degrees(math.atan2(self.current_vertical_velocity,
                                                         self.current_horizontal_velocity)), 5)

    def update_acceleration(self):
        if self.air_resistance_enabled:
            self.current_horizontal_acceleration = self.data_lists['xa'][self.time_index]
            self.current_vertical_acceleration = self.data_lists['ya'][self.time_index]
        else:
            self.current_horizontal_acceleration = 0
            self.current_vertical_acceleration = - self.gravity

        self.current_total_acceleration = round(math.sqrt(self.current_horizontal_acceleration ** 2 \
                                                    + self.current_vertical_acceleration ** 2), 5)
        self.current_acceleration_direction = round(math.degrees(math.atan2(self.current_vertical_acceleration,
                                                         self.current_horizontal_acceleration)), 5)

    def update_energy(self):
        self.current_kinetic_energy = round(0.5 * self.mass * self.current_total_velocity ** 2, 5)
        self.current_gravitational_potential_energy = round(self.gravity * self.mass * self.current_height, 5)
        self.current_total_energy = round(self.current_kinetic_energy + self.current_gravitational_potential_energy, 5)
        self.energy_loss = round(self.initial_total_energy - self.current_total_energy, 0)
