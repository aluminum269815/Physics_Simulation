from constants import *


class Settings:
    def __init__(self):
        self.gravity = DEFAULT_GRAVITY
        self.air_resistance_enabled = False
        self.air_density = DEFAULT_AIR_DENSITY
        self.drag_coefficient = DEFAULT_DRAG_COEFFICIENT

        self.cannon_height = DEFAULT_CANNON_HEIGHT
        self.firing_angle = DEFAULT_FIRING_ANGLE
        self.initial_cannon_velocity = DEFAULT_CANNON_INITIAL_VELOCITY

        self.cannonball_mass = DEFAULT_CANNONBALL_MASS
        self.cannonball_radius = DEFAULT_CANNONBALL_RADIUS

        self.time_after_firing = 0
        self.paused = True
        self.displaying_speed = 1

        self.all_cannonball_selected = False
        self.selecting_cannonball = None
