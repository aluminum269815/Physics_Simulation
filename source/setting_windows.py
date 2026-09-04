from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt

from constants import *


class SettingWindow(QWidget):
    name = None

    def __init__(self, program):
        super().__init__(program, Qt.Window)
        self.program = program
        self.settings = self.program.settings
        self.setWindowTitle(self.name)
        self.setFixedSize(*SETTING_WINDOW_SIZES[self.name])
        self.setStyleSheet('font-family: Arial')

        flags = self.windowFlags()
        flags &= ~Qt.WindowMinimizeButtonHint & ~Qt.WindowMaximizeButtonHint
        self.setWindowFlags(flags)

    def update_information(self):
        pass


class BasicParameters(SettingWindow):
    name = 'Basic Parameters'

    def __init__(self, program):
        super().__init__(program)


        air_resistance_label = QLabel('Air Resistance')

        self.air_resistance_checkbox = QCheckBox()
        self.air_resistance_checkbox.setChecked(self.settings.air_resistance_enabled)
        self.air_resistance_checkbox.stateChanged.connect(self.change_air_resistance_enabled)


        air_density_label = QLabel('Air Density')

        self.air_density_slider = QSlider(Qt.Horizontal)
        self.air_density_slider.setRange(0, int(MAX_SLIDER_AIR_DENSITY * 1000))
        self.air_density_slider.setValue(int(self.settings.air_density * 1000))
        self.air_density_slider.sliderMoved.connect(self.change_slider_air_density)

        self.air_density_input = QLineEdit()
        self.air_density_input.setText(str(self.settings.air_density))
        self.air_density_input.setFixedWidth(60)
        self.air_density_input.editingFinished.connect(self.change_input_air_density)

        air_density_unit_label = QLabel('kg/m<sup>-3<sup>')


        gravity_label = QLabel('Gravity (downward acceleration)')

        self.gravity_slider = QSlider(Qt.Horizontal)
        self.gravity_slider.setRange(int(MIN_GRAVITY * 100), int(MAX_SLIDER_GRAVITY * 100))
        self.gravity_slider.setValue(int(self.settings.gravity * 100))
        self.gravity_slider.sliderMoved.connect(self.change_slider_gravity)

        self.gravity_input = QLineEdit()
        self.gravity_input.setText(str(self.settings.gravity))
        self.gravity_input.setFixedWidth(60)
        self.gravity_input.editingFinished.connect(self.change_input_gravity)

        gravity_unit_label = QLabel("m/s<sup>-2<sup> ")


        layout = QVBoxLayout()

        air_resistance_row = QHBoxLayout()
        air_resistance_row.addWidget(air_resistance_label)
        air_resistance_row.addWidget(self.air_resistance_checkbox)
        air_resistance_row.addStretch(4)
        layout.addLayout(air_resistance_row)

        layout.addWidget(air_density_label)
        air_density_row = QHBoxLayout()
        air_density_row.addWidget(self.air_density_slider)
        air_density_row.addWidget(self.air_density_input)
        air_density_row.addWidget(air_density_unit_label)
        layout.addLayout(air_density_row)

        layout.addWidget(gravity_label)
        gravity_row = QHBoxLayout()
        gravity_row.addWidget(self.gravity_slider)
        gravity_row.addWidget(self.gravity_input)
        gravity_row.addWidget(gravity_unit_label)
        layout.addLayout(gravity_row)

        self.setLayout(layout)

    def change_air_resistance_enabled(self, state):
        self.settings.set_air_resistance_enabled(state == Qt.Checked)

    def change_slider_air_density(self, value):
        air_density = round(value / 1000, 3)
        self.settings.set_air_density(air_density)
        self.update_air_density()

    def change_input_air_density(self):
        try:
            air_density = round(float(self.air_density_input.text()), 3)
            self.settings.set_air_density(air_density)
        except ValueError:
            pass
        self.update_air_density()

    def update_air_density(self):
        self.air_density_slider.setValue(int(self.settings.air_density * 1000))
        self.air_density_input.setText(str(self.settings.air_density))

    def change_slider_gravity(self, value):
        gravity = round(value / 100, 2)
        self.settings.set_gravity(gravity)
        self.update_gravity()

    def change_input_gravity(self):
        try:
            gravity = round(float(self.gravity_input.text()), 2)
            self.settings.set_gravity(gravity)
        except ValueError:
            pass
        self.update_gravity()

    def update_gravity(self):
        self.gravity_slider.setValue(int(self.settings.gravity * 100))
        self.gravity_input.setText(str(self.settings.gravity))

    def update_information(self):
        self.update_air_density()
        self.update_gravity()


class VisualDisplay(SettingWindow):
    name = 'Visual Display'

    def __init__(self, program):
        super().__init__(program)

        trajectory_label = QLabel('Show Trajectory')
        self.trajectory_checkbox = QCheckBox()
        self.trajectory_checkbox.setChecked(self.settings.showing_trajectory)
        self.trajectory_checkbox.stateChanged.connect(self.change_showing_trajectory)

        acceleration_arrows_label = QLabel("Show Acceleration Arrows")
        self.acceleration_arrows_checkbox = QCheckBox()
        self.acceleration_arrows_checkbox.setChecked(self.settings.showing_acceleration_arrows)
        self.acceleration_arrows_checkbox.stateChanged.connect(self.change_showing_acceleration_arrows)

        velocity_arrows_label = QLabel("Show Velocity Arrows")
        self.velocity_arrows_checkbox = QCheckBox()
        self.velocity_arrows_checkbox.setChecked(self.settings.showing_velocity_arrows)
        self.velocity_arrows_checkbox.stateChanged.connect(self.change_showing_velocity_arrows)

        layout = QVBoxLayout()

        trajectory_row = QHBoxLayout()
        trajectory_row.addWidget(trajectory_label)
        trajectory_row.addWidget(self.trajectory_checkbox)
        layout.addLayout(trajectory_row)

        acceleration_arrows_row = QHBoxLayout()
        acceleration_arrows_row.addWidget(acceleration_arrows_label)
        acceleration_arrows_row.addWidget(self.acceleration_arrows_checkbox)
        layout.addLayout(acceleration_arrows_row)

        velocity_arrows_row = QHBoxLayout()
        velocity_arrows_row.addWidget(velocity_arrows_label)
        velocity_arrows_row.addWidget(self.velocity_arrows_checkbox)
        layout.addLayout(velocity_arrows_row)

        self.setLayout(layout)

    def change_showing_trajectory(self, state):
        self.settings.set_showing_trajectory(state == Qt.Checked)

    def change_showing_acceleration_arrows(self, state):
        self.settings.set_showing_acceleration_arrows(state == Qt.Checked)

    def change_showing_velocity_arrows(self, state):
        self.settings.set_showing_velocity_arrows(state == Qt.Checked)


class CannonSettings(SettingWindow):
    name = 'Cannon Settings'

    def __init__(self, program):
        super().__init__(program)

        initial_velocity_label = QLabel("Initial Velocity")

        self.initial_velocity_slider = QSlider(Qt.Horizontal)
        self.initial_velocity_slider.setRange(int(MIN_INITIAL_VELOCITY * 10), int(MAX_SLIDER_INITIAL_VELOCITY * 10))
        self.initial_velocity_slider.setValue(int(self.settings.initial_velocity * 10))
        self.initial_velocity_slider.sliderMoved.connect(self.change_slider_initial_velocity)

        self.initial_velocity_input = QLineEdit()
        self.initial_velocity_input.setText(str(self.settings.initial_velocity))
        self.initial_velocity_input.setFixedWidth(60)
        self.initial_velocity_input.editingFinished.connect(self.change_input_initial_velocity)

        initial_velocity_unit_label = QLabel("m/s<sup>-1</sup>")


        cannonball_mass_label = QLabel("Cannonball Mass")

        self.cannonball_mass_slider = QSlider(Qt.Horizontal)
        self.cannonball_mass_slider.setRange(int(MIN_CANNONBALL_MASS * 10), int(MAX_SLIDER_CANNONBALL_MASS * 10))
        self.cannonball_mass_slider.setValue(int(self.settings.cannonball_mass * 10))
        self.cannonball_mass_slider.sliderMoved.connect(self.change_slider_cannonball_mass)

        self.cannonball_mass_input = QLineEdit()
        self.cannonball_mass_input.setText(str(self.settings.cannonball_mass))
        self.cannonball_mass_input.setFixedWidth(60)
        self.cannonball_mass_input.editingFinished.connect(self.change_input_cannonball_mass)

        cannonball_mass_unit_label = QLabel(" kg   ")


        cannon_height_label = QLabel("Cannon Height")

        self.cannon_height_slider = QSlider(Qt.Horizontal)
        self.cannon_height_slider.setRange(0, int(MAX_CANNON_HEIGHT * 10))
        self.cannon_height_slider.setValue(int(self.settings.cannon_height * 10))
        self.cannon_height_slider.sliderMoved.connect(self.change_slider_cannon_height)

        self.cannon_height_input = QLineEdit()
        self.cannon_height_input.setText(str(self.settings.cannon_height * 10))
        self.cannon_height_input.setFixedWidth(60)
        self.cannon_height_input.editingFinished.connect(self.change_input_cannon_height)

        cannon_height_unit_label = QLabel(" m   ")


        cannonball_radius_label = QLabel("Cannonball Radius")

        self.cannonball_radius_slider = QSlider(Qt.Horizontal)
        self.cannonball_radius_slider.setRange(int(MIN_CANNONBALL_RADIUS * 10), int(MAX_SLIDER_CANNONBALL_RADIUS * 10))
        self.cannonball_radius_slider.setValue(int(self.settings.cannonball_radius * 10))
        self.cannonball_radius_slider.sliderMoved.connect(self.change_slider_cannonball_radius)

        self.cannonball_radius_input = QLineEdit()
        self.cannonball_radius_input.setText(str(self.settings.cannonball_radius))
        self.cannonball_radius_input.setFixedWidth(60)
        self.cannonball_radius_input.editingFinished.connect(self.change_input_cannonball_radius)

        cannonball_radius_unit_label = QLabel(" m   ")


        firing_angle_label = QLabel("Firing Angle")

        self.firing_angle_slider = QSlider(Qt.Horizontal)
        self.firing_angle_slider.setRange(MIN_FIRING_ANGLE, MAX_FIRING_ANGLE)
        self.firing_angle_slider.setValue(self.settings.firing_angle)
        self.firing_angle_slider.sliderMoved.connect(self.change_slider_firing_angle)

        self.firing_angle_input = QLineEdit()
        self.firing_angle_input.setText(str(self.settings.firing_angle))
        self.firing_angle_input.setFixedWidth(60)
        self.firing_angle_input.editingFinished.connect(self.change_input_firing_angle)

        firing_angle_unit_label = QLabel("\u00B0    ")


        layout = QVBoxLayout()

        layout.addWidget(initial_velocity_label)
        initial_velocity_row = QHBoxLayout()
        initial_velocity_row.addWidget(self.initial_velocity_slider)
        initial_velocity_row.addWidget(self.initial_velocity_input)
        initial_velocity_row.addWidget(initial_velocity_unit_label)
        layout.addLayout(initial_velocity_row)

        layout.addWidget(cannonball_mass_label)
        cannonball_mass_row = QHBoxLayout()
        cannonball_mass_row.addWidget(self.cannonball_mass_slider)
        cannonball_mass_row.addWidget(self.cannonball_mass_input)
        cannonball_mass_row.addWidget(cannonball_mass_unit_label)
        layout.addLayout(cannonball_mass_row)

        layout.addWidget(cannon_height_label)
        cannon_height_row = QHBoxLayout()
        cannon_height_row.addWidget(self.cannon_height_slider)
        cannon_height_row.addWidget(self.cannon_height_input)
        cannon_height_row.addWidget(cannon_height_unit_label)
        layout.addLayout(cannon_height_row)

        layout.addWidget(cannonball_radius_label)
        cannonball_radius_row = QHBoxLayout()
        cannonball_radius_row.addWidget(self.cannonball_radius_slider)
        cannonball_radius_row.addWidget(self.cannonball_radius_input)
        cannonball_radius_row.addWidget(cannonball_radius_unit_label)
        layout.addLayout(cannonball_radius_row)

        layout.addWidget(firing_angle_label)
        firing_angle_row = QHBoxLayout()
        firing_angle_row.addWidget(self.firing_angle_slider)
        firing_angle_row.addWidget(self.firing_angle_input)
        firing_angle_row.addWidget(firing_angle_unit_label)
        layout.addLayout(firing_angle_row)

        self.setLayout(layout)

    def change_slider_initial_velocity(self, value):
        self.program.change_initial_velocity(round(value / 10, 1))

    def change_input_initial_velocity(self):
        try:
            velocity = round(float(self.initial_velocity_input.text()), 1)
            self.program.change_initial_velocity(velocity)
        except ValueError:
            self.update_initial_velocity()

    def update_initial_velocity(self):
        self.initial_velocity_slider.setValue(int(self.settings.initial_velocity * 10))
        self.initial_velocity_input.setText(str(self.settings.initial_velocity))

    def change_slider_cannonball_mass(self, value):
        self.settings.set_cannonball_mass(round(value / 10, 1))
        self.update_cannonball_mass()

    def change_input_cannonball_mass(self):
        try:
            cannonball_mass = round(float(self.cannonball_mass_input.text()), 1)
            self.settings.set_cannonball_mass(cannonball_mass)
        except ValueError:
            pass
        self.update_cannonball_mass()

    def update_cannonball_mass(self):
        self.cannonball_mass_slider.setValue(int(self.settings.cannonball_mass * 10))
        self.cannonball_mass_input.setText(str(self.settings.cannonball_mass))

    def change_slider_cannon_height(self, value):
        self.program.change_cannon_height(round(value / 10, 1))

    def change_input_cannon_height(self):
        try:
            height = round(float(self.cannon_height_input.text()), 1)
            self.program.change_cannon_height(height)
        except ValueError:
            self.update_cannon_height()

    def update_cannon_height(self):
        self.cannon_height_slider.setValue(int(self.settings.cannon_height * 10))
        self.cannon_height_input.setText(str(self.settings.cannon_height))

    def change_slider_cannonball_radius(self, value):
        self.settings.set_cannonball_radius(round(value / 10, 1))
        self.update_cannonball_radius()

    def change_input_cannonball_radius(self):
        try:
            radius = round(float(self.cannonball_radius_input.text()), 1)
            self.settings.set_cannonball_radius(radius)
        except ValueError:
            pass
        self.update_cannonball_radius()

    def update_cannonball_radius(self):
        self.cannonball_radius_slider.setValue(int(self.settings.cannonball_radius * 10))
        self.cannonball_radius_input.setText(str(self.settings.cannonball_radius))

    def change_slider_firing_angle(self, value):
        self.program.change_firing_angle(value)

    def change_input_firing_angle(self):
        try:
            angle = int(self.firing_angle_input.text())
            self.program.change_firing_angle(angle)
        except ValueError:
            self.update_firing_angle()

    def update_firing_angle(self):
        self.firing_angle_slider.setValue(int(self.settings.firing_angle))
        self.firing_angle_input.setText(str(self.settings.firing_angle))

    def update_information(self):
        self.update_initial_velocity()
        self.update_firing_angle()
        self.update_cannon_height()
        self.update_cannonball_mass()
        self.update_cannonball_radius()


class CannonballDetails(SettingWindow):
    name = 'Cannonball Details'

    def __init__(self, program):
        super().__init__(program)

        layout = QVBoxLayout()

        row = QHBoxLayout()
        row.addWidget(QLabel('Gravity:'), 2, alignment=Qt.AlignRight)
        self.gravity_info = QLabel('__ m/s<sup>-2</sup>')
        row.addWidget(self.gravity_info, 1, alignment=Qt.AlignHCenter)
        layout.addLayout(row)

        row = QHBoxLayout()
        row.addWidget(QLabel('Air resistance enabled:'), 2, alignment=Qt.AlignRight)
        self.air_resistance_enabled_info = QLabel('N/A')
        row.addWidget(self.air_resistance_enabled_info, 1, alignment=Qt.AlignHCenter)
        layout.addLayout(row)

        row = QHBoxLayout()
        row.addWidget(QLabel('Air Density:'), 2, alignment=Qt.AlignRight)
        self.air_density_info = QLabel('__ kg/m<sup>-3<sup>')
        row.addWidget(self.air_density_info, 1, alignment=Qt.AlignHCenter)
        layout.addLayout(row)

        layout.addStretch()

        row = QHBoxLayout()
        row.addWidget(QLabel('Mass:'), 2, alignment=Qt.AlignRight)
        self.mass_info = QLabel('__ kg')
        row.addWidget(self.mass_info, 1, alignment=Qt.AlignHCenter)
        layout.addLayout(row)

        row = QHBoxLayout()
        row.addWidget(QLabel('Radius:'), 2, alignment=Qt.AlignRight)
        self.radius_info = QLabel('__ m')
        row.addWidget(self.radius_info, 1, alignment=Qt.AlignHCenter)
        layout.addLayout(row)

        row = QHBoxLayout()
        row.addWidget(QLabel('Firing Time:'), 2, alignment=Qt.AlignRight)
        self.firing_time_info = QLabel('__ s')
        row.addWidget(self.firing_time_info, 1, alignment=Qt.AlignHCenter)
        layout.addLayout(row)

        row = QHBoxLayout()
        row.addWidget(QLabel('Time After Firing:'), 2, alignment=Qt.AlignRight)
        self.time_after_firing_info = QLabel('__ s')
        row.addWidget(self.time_after_firing_info, 1, alignment=Qt.AlignHCenter)
        layout.addLayout(row)

        layout.addStretch()

        row = QHBoxLayout()
        row.addWidget(QLabel('Initial Height:'), 2, alignment=Qt.AlignRight)
        self.initial_height_info = QLabel('__ m')
        row.addWidget(self.initial_height_info, 1, alignment=Qt.AlignHCenter)
        layout.addLayout(row)

        row = QHBoxLayout()
        row.addWidget(QLabel('Current Distance:'), 2, alignment=Qt.AlignRight)
        self.current_distance_info = QLabel('__ m')
        row.addWidget(self.current_distance_info, 1, alignment=Qt.AlignHCenter)
        layout.addLayout(row)

        row = QHBoxLayout()
        row.addWidget(QLabel('Current Height:'), 2, alignment=Qt.AlignRight)
        self.current_height_info = QLabel('__ m')
        row.addWidget(self.current_height_info, 1, alignment=Qt.AlignHCenter)
        layout.addLayout(row)

        layout.addStretch()

        row = QHBoxLayout()
        row.addWidget(QLabel('Initial Total Velocity:'), 2, alignment=Qt.AlignRight)
        self.initial_total_velocity_info = QLabel('__ m/s<sup>-1</sup>')
        row.addWidget(self.initial_total_velocity_info, 1, alignment=Qt.AlignHCenter)
        layout.addLayout(row)

        row = QHBoxLayout()
        row.addWidget(QLabel('Initial Moving Direction:'), 2, alignment=Qt.AlignRight)
        self.initial_moving_direction_info = QLabel('__ \u00B0')
        row.addWidget(self.initial_moving_direction_info, 1, alignment=Qt.AlignHCenter)
        layout.addLayout(row)

        row = QHBoxLayout()
        row.addWidget(QLabel('Initial Horizontal Velocity:'), 2, alignment=Qt.AlignRight)
        self.initial_horizontal_velocity_info = QLabel('__ m/s<sup>-1</sup>')
        row.addWidget(self.initial_horizontal_velocity_info, 1, alignment=Qt.AlignHCenter)
        layout.addLayout(row)

        row = QHBoxLayout()
        row.addWidget(QLabel('Initial Vertical Velocity:'), 2, alignment=Qt.AlignRight)
        self.initial_vertical_velocity_info = QLabel('__ m/s<sup>-1</sup>')
        row.addWidget(self.initial_vertical_velocity_info, 1, alignment=Qt.AlignHCenter)
        layout.addLayout(row)

        layout.addStretch()

        row = QHBoxLayout()
        row.addWidget(QLabel('Current Total Velocity:'), 2, alignment=Qt.AlignRight)
        self.current_total_velocity_info = QLabel('__ m/s<sup>-1</sup>')
        row.addWidget(self.current_total_velocity_info, 1, alignment=Qt.AlignHCenter)
        layout.addLayout(row)

        row = QHBoxLayout()
        row.addWidget(QLabel('Current Moving Direction:'), 2, alignment=Qt.AlignRight)
        self.current_moving_direction_info = QLabel('__ \u00B0')
        row.addWidget(self.current_moving_direction_info, 1, alignment=Qt.AlignHCenter)
        layout.addLayout(row)

        row = QHBoxLayout()
        row.addWidget(QLabel('Current Horizontal Velocity:'), 2, alignment=Qt.AlignRight)
        self.current_horizontal_velocity_info = QLabel('__ m/s<sup>-1</sup>')
        row.addWidget(self.current_horizontal_velocity_info, 1, alignment=Qt.AlignHCenter)
        layout.addLayout(row)

        row = QHBoxLayout()
        row.addWidget(QLabel('Current Vertical Velocity:'), 2, alignment=Qt.AlignRight)
        self.current_vertical_velocity_info = QLabel('__ m/s<sup>-1</sup>')
        row.addWidget(self.current_vertical_velocity_info, 1, alignment=Qt.AlignHCenter)
        layout.addLayout(row)

        layout.addStretch()

        row = QHBoxLayout()
        row.addWidget(QLabel('Current Total Acceleration:'), 2, alignment=Qt.AlignRight)
        self.current_total_acceleration_info = QLabel('__ m/s<sup>-2</sup>')
        row.addWidget(self.current_total_acceleration_info, 1, alignment=Qt.AlignHCenter)
        layout.addLayout(row)

        row = QHBoxLayout()
        row.addWidget(QLabel('Current Accelerating Direction:'), 2, alignment=Qt.AlignRight)
        self.current_accelerating_direction_info = QLabel('__ \u00B0')
        row.addWidget(self.current_accelerating_direction_info, 1, alignment=Qt.AlignHCenter)
        layout.addLayout(row)

        row = QHBoxLayout()
        row.addWidget(QLabel('Current Horizontal Acceleration:'), 2, alignment=Qt.AlignRight)
        self.current_horizontal_acceleration_info = QLabel('__ m/s<sup>-2</sup>')
        row.addWidget(self.current_horizontal_acceleration_info, 1, alignment=Qt.AlignHCenter)
        layout.addLayout(row)

        row = QHBoxLayout()
        row.addWidget(QLabel('Current Vertical Acceleration:'), 2, alignment=Qt.AlignRight)
        self.current_vertical_acceleration_info = QLabel('__ m/s<sup>-2</sup>')
        row.addWidget(self.current_vertical_acceleration_info, 1, alignment=Qt.AlignHCenter)
        layout.addLayout(row)

        layout.addStretch()

        row = QHBoxLayout()
        row.addWidget(QLabel('Initial Kinetic Energy:'), 2, alignment=Qt.AlignRight)
        self.initial_kinetic_energy_info = QLabel('__ J')
        row.addWidget(self.initial_kinetic_energy_info, 1, alignment=Qt.AlignHCenter)
        layout.addLayout(row)

        row = QHBoxLayout()
        row.addWidget(QLabel('Initial Gravitational Potential Energy:'), 2, alignment=Qt.AlignRight)
        self.initial_gravitational_potential_energy_info = QLabel('__ J')
        row.addWidget(self.initial_gravitational_potential_energy_info, 1, alignment=Qt.AlignHCenter)
        layout.addLayout(row)

        row = QHBoxLayout()
        row.addWidget(QLabel('Initial Total Energy:'), 2, alignment=Qt.AlignRight)
        self.initial_total_energy_info = QLabel('__ J')
        row.addWidget(self.initial_total_energy_info, 1, alignment=Qt.AlignHCenter)
        layout.addLayout(row)

        row = QHBoxLayout()
        row.addWidget(QLabel('Current Kinetic Energy:'), 2, alignment=Qt.AlignRight)
        self.current_kinetic_energy_info = QLabel('__ J')
        row.addWidget(self.current_kinetic_energy_info, 1, alignment=Qt.AlignHCenter)
        layout.addLayout(row)

        row = QHBoxLayout()
        row.addWidget(QLabel('Current Gravitational Potential Energy:'), 2, alignment=Qt.AlignRight)
        self.current_gravitational_potential_energy_info = QLabel('__ J')
        row.addWidget(self.current_gravitational_potential_energy_info, 1, alignment=Qt.AlignHCenter)
        layout.addLayout(row)

        row = QHBoxLayout()
        row.addWidget(QLabel('Current Total Energy:'), 2, alignment=Qt.AlignRight)
        self.current_total_energy_info = QLabel('__ J')
        row.addWidget(self.current_total_energy_info, 1, alignment=Qt.AlignHCenter)
        layout.addLayout(row)

        row = QHBoxLayout()
        row.addWidget(QLabel('Energy Loss:'), 2, alignment=Qt.AlignRight)
        self.energy_loss_info = QLabel('__ J')
        row.addWidget(self.energy_loss_info, 1, alignment=Qt.AlignHCenter)
        layout.addLayout(row)

        self.setLayout(layout)

    def update_information(self):
        cannonball = self.program.selecting_cannonball

        if cannonball:
            self.gravity_info.setText(f'{cannonball.gravity:.2f} m/s<sup>-2</sup>')
            self.air_resistance_enabled_info.setText('Yes' if cannonball.air_resistance_enabled else 'No')
            self.air_density_info.setText(f'{cannonball.air_density:.3f} kg/m<sup>-3<sup>' if cannonball.air_resistance_enabled else 'N/A')

            self.mass_info.setText(f'{cannonball.mass:.2f} kg')
            self.radius_info.setText(f'{cannonball.radius:.2f} m')
            self.firing_time_info.setText(f'{cannonball.firing_time:.2f} s')
            self.time_after_firing_info.setText(f'{cannonball.time_after_firing:.2f} s')

            self.initial_height_info.setText(f'{cannonball.initial_height:.2f} m')
            self.current_distance_info.setText(f'{cannonball.current_distance:.2f} m')
            self.current_height_info.setText(f'{cannonball.current_height:.2f} m')

            self.initial_total_velocity_info.setText(f'{cannonball.initial_total_velocity:.2f} m/s<sup>-1</sup>')
            self.initial_moving_direction_info.setText(f'{cannonball.initial_moving_direction:.0f} \u00B0')
            self.initial_horizontal_velocity_info.setText(f'{cannonball.initial_total_velocity:.2f} m/s<sup>-1</sup>')
            self.initial_vertical_velocity_info.setText(f'{cannonball.initial_total_velocity:.2f} m/s<sup>-1</sup>')

            self.current_total_velocity_info.setText(f'{cannonball.current_total_velocity:.2f} m/s<sup>-1</sup>')
            self.current_moving_direction_info.setText(f'{cannonball.current_moving_direction:.0f} \u00B0')
            self.current_horizontal_velocity_info.setText(f'{cannonball.current_horizontal_velocity:.2f} m/s<sup>-1</sup>')
            self.current_vertical_velocity_info.setText(f'{cannonball.current_vertical_velocity:.2f} m/s<sup>-1</sup>')

            self.current_total_acceleration_info.setText(f'{cannonball.current_total_acceleration:.2f} m/s<sup>-2</sup>')
            self.current_accelerating_direction_info.setText(f'{cannonball.current_accelerating_direction:.0f} \u00B0')
            self.current_horizontal_acceleration_info.setText(f'{cannonball.current_horizontal_acceleration:.2f} m/s<sup>-2</sup>')
            self.current_vertical_acceleration_info.setText(f'{cannonball.current_vertical_acceleration:.2f} m/s<sup>-2</sup>')

            self.initial_kinetic_energy_info.setText(f'{cannonball.initial_kinetic_energy:.0f} J')
            self.initial_gravitational_potential_energy_info.setText(f'{cannonball.initial_gravitational_potential_energy:.0f} J')
            self.initial_total_energy_info.setText(f'{cannonball.initial_total_energy:.0f} J')
            self.current_kinetic_energy_info.setText(f'{cannonball.current_kinetic_energy:.0f} J')
            self.current_gravitational_potential_energy_info.setText(f'{cannonball.current_gravitational_potential_energy:.0f} J')
            self.current_total_energy_info.setText(f'{cannonball.current_total_energy:.0f} J')
            self.energy_loss_info.setText(f'{cannonball.energy_loss:.0f} J')

        else:
            self.gravity_info.setText('__ m/s<sup>-2</sup>')
            self.air_resistance_enabled_info.setText('N/A')
            self.air_density_info.setText('__ kg/m<sup>-3<sup>')

            self.mass_info.setText('__ kg')
            self.radius_info.setText('__ m')
            self.firing_time_info.setText('__ s')
            self.time_after_firing_info.setText('__ s')

            self.initial_height_info.setText('__ m')
            self.current_distance_info.setText('__ m')
            self.current_height_info.setText('__ m')

            self.initial_total_velocity_info.setText('__ m/s<sup>-1</sup>')
            self.initial_moving_direction_info.setText('__ \u00B0')
            self.initial_horizontal_velocity_info.setText('__ m/s<sup>-1</sup>')
            self.initial_vertical_velocity_info.setText('__ m/s<sup>-1</sup>')

            self.current_total_velocity_info.setText('__ m/s<sup>-1</sup>')
            self.current_moving_direction_info.setText('__ \u00B0')
            self.current_horizontal_velocity_info.setText('__ m/s<sup>-1</sup>')
            self.current_vertical_velocity_info.setText('__ m/s<sup>-1</sup>')

            self.current_total_acceleration_info.setText('__ m/s<sup>-2</sup>')
            self.current_accelerating_direction_info.setText('__ \u00B0')
            self.current_horizontal_acceleration_info.setText('__ m/s<sup>-2</sup>')
            self.current_vertical_acceleration_info.setText('__ m/s<sup>-2</sup>')

            self.initial_kinetic_energy_info.setText('__ J')
            self.initial_gravitational_potential_energy_info.setText('__ J')
            self.initial_total_energy_info.setText('__ J')
            self.current_kinetic_energy_info.setText('__ J')
            self.current_gravitational_potential_energy_info.setText('__ J')
            self.current_total_energy_info.setText('__ J')
            self.energy_loss_info.setText('__ J')
