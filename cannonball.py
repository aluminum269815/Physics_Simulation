import math

class CannonBall:
    def __init__(self, program):
        self.program = program
        settings = self.program.settings

        self.time_after_firing = 0

        self.mass = settings.cannonball_mass
        self.radius = settings.cannonball_radius

        self.initial_height = settings.cannon_height
        self.initial_total_velocity = settings.initial_cannon_velocity
        self.initial_moving_direction = settings.firing_angle
        self.initial_horizontal_velocity = round(self.initial_height * math.cos(self.initial_moving_direction), 3)
        self.initial_vertical_velocity = round(self.initial_height * math.sin(self.initial_moving_direction), 3)

        self.initial_kinetic_energy = round(0.5 * self.mass * self.initial_total_velocity ** 2, 0)
        self.initial_gravitational_potential_energy = round(9.8 * self.mass * self.initial_height, 0)
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

        self.update_data()

    def update(self):
        self.update_data()

    def update_data(self):
        self.update_position()
        self.update_velocity()
        self.update_acceleration()
        self.update_energy()

    def update_position(self):
        self.current_distance = round(self.initial_horizontal_velocity * self.time_after_firing, 3)
        self.current_height = round(self.initial_height + self.time_after_firing * self.initial_vertical_velocity \
                              - 4.9 * self.time_after_firing ** 2, 3)

    def update_velocity(self):
        self.current_horizontal_velocity = self.initial_horizontal_velocity
        self.current_vertical_velocity = round(self.initial_vertical_velocity - 9.8 * self.time_after_firing, 3)

        self.current_total_velocity = round(math.sqrt(self.current_horizontal_velocity ** 2 \
                                                    + self.current_vertical_velocity ** 2), 3)
        self.current_moving_direction = round(math.degrees(math.atan2(self.current_vertical_velocity,
                                                         self.current_horizontal_velocity)), 3)

    def update_acceleration(self):
        self.current_horizontal_acceleration = 0
        self.current_vertical_acceleration = -9.8

        self.current_total_acceleration = round(math.sqrt(self.current_horizontal_acceleration ** 2 \
                                                    + self.current_vertical_acceleration ** 2), 3)
        self.current_acceleration_direction = round(math.degrees(math.atan2(self.current_vertical_acceleration,
                                                         self.current_horizontal_acceleration)), 3)

    def update_energy(self):
        self.current_kinetic_energy = round(0.5 * self.mass * self.current_total_velocity ** 2, 0)
        self.current_gravitational_potential_energy = round(9.8 * self.mass * self.current_height, 0)
        self.current_total_energy = round(self.current_kinetic_energy + self.current_gravitational_potential_energy, 0)
        self.energy_loss = round(self.initial_total_energy - self.current_total_energy, 0)

    def test(self, time):
        self.time_after_firing = time
        self.update_data()
        for key, value in vars(self).items():
            print(f"{key}: {value}")

a = CannonBall()
a.test(7)
