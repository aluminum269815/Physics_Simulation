class CannonBall:
    def __init__(self):
        self.time_after_firing = 0

        self.mass = 10
        self.radius = 10

        self.initial_height = 100
        self.initial_total_velocity = 28.28427
        self.initial_moving_direction = 45
        self.initial_horizontal_velocity = 20
        self.initial_vertical_velocity = 20

        self.initial_kinetic_energy = 0.5 * self.mass * self.initial_total_velocity ** 2
        self.initial_gravitational_potential_energy = 9.8 * self.mass * self.initial_height
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

    def update(self):
        self.update_data()

    def update_data(self):
        self.update_position()
        self.update_velocity()
        self.update_acceleration()
        self.update_energy()

    def update_position(self):
        pass

    def update_velocity(self):
        pass

    def update_acceleration(self):
        pass

    def update_energy(self):
        pass
