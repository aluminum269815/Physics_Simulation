from constants import *


class Settings:
    def __init__(self):
        self.gravity = DEFAULT_GRAVITY
        self.air_resistance_enabled = True
        self.air_density = DEFAULT_AIR_DENSITY
        self.drag_coefficient = DEFAULT_DRAG_COEFFICIENT

        self.cannon_height = DEFAULT_CANNON_HEIGHT
        self.firing_angle = DEFAULT_FIRING_ANGLE
        self.initial_velocity = DEFAULT_CANNON_INITIAL_VELOCITY

        self.cannonball_mass = DEFAULT_CANNONBALL_MASS
        self.cannonball_radius = DEFAULT_CANNONBALL_RADIUS

        self.target_distance = 50
        self.target_height = 50
        self.showing_target_label = True

        self.time = 0
        self.max_time = 0
        self.paused = False
        self.playing_speed = 1.0

        self.all_cannonball_selected = False
        self.selecting_cannonball = None

        self.showing_trajectory = True
        self.showing_velocity_arrows = False
        self.showing_acceleration_arrows = False

    def reset(self):
        self.gravity = DEFAULT_GRAVITY
        self.air_resistance_enabled = True
        self.air_density = DEFAULT_AIR_DENSITY
        self.drag_coefficient = DEFAULT_DRAG_COEFFICIENT

        self.cannon_height = DEFAULT_CANNON_HEIGHT
        self.firing_angle = DEFAULT_FIRING_ANGLE
        self.initial_velocity = DEFAULT_CANNON_INITIAL_VELOCITY

        self.cannonball_mass = DEFAULT_CANNONBALL_MASS
        self.cannonball_radius = DEFAULT_CANNONBALL_RADIUS

    def set_gravity(self, gravity):
        self.gravity = min(max(gravity, MIN_GRAVITY), MAX_GRAVITY)

    def set_air_resistance_enabled(self, enabled):
        self.air_resistance_enabled = enabled

    def set_air_density(self, air_density):
        self.air_density = min(max(air_density, 0), MAX_AIR_DENSITY)

    def set_cannon_height(self, height):
        self.cannon_height = min(max(height, 0), MAX_CANNON_HEIGHT)

    def set_firing_angle(self, angle):
        self.firing_angle = min(max(angle, MIN_FIRING_ANGLE), MAX_FIRING_ANGLE)

    def set_initial_velocity(self, velocity):
        self.initial_velocity = min(max(velocity, MIN_INITIAL_VELOCITY), MAX_INITIAL_VELOCITY)

    def set_cannonball_mass(self, mass):
        self.cannonball_mass = min(max(mass, MIN_CANNONBALL_MASS), MAX_CANNONBALL_MASS)

    def set_cannonball_radius(self, radius):
        self.cannonball_radius = min(max(radius, MIN_CANNONBALL_RADIUS), MAX_CANNONBALL_RADIUS)

    def set_target_position(self, distance, height):
        self.target_distance = min(max(distance, 0), MAX_TARGET_DISTANCE)
        self.target_height = min(max(height, 0), MAX_TARGET_HEIGHT)

    def set_time(self, time):
        self.time = min(time, self.max_time)

    def set_max_time(self, max_time):
        self.max_time = max_time
        if self.time > self.max_time:
            self.time = self.max_time

    def set_showing_trajectory(self, showing):
        self.showing_trajectory = showing

    def set_showing_velocity_arrows(self, showing):
        self.showing_velocity_arrows = showing

    def set_showing_acceleration_arrows(self, showing):
        self.showing_acceleration_arrows = showing
