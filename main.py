import os, sys

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from settings import Settings
from basicparameters import BasicParameters
from visualdisplay import VisualDisplay
from cannonsettings import CannonSettings
from cannonballdetails import CannonballDetails
class Program(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Projectile Motion sim")
        self.background = QPixmap(os.path.abspath("asset/background.png"))
        self.resize(700, 500)

        self.settings = Settings()
        self.settings_window = None

        self.settings_panel = QPushButton("⚙ Settings    ▼")
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
            }
    
            QPushButton:hover {
                background-color: #eeeeee;
                font-family: Arial;
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
            self.settings_panel.setText("⚙ Settings    ▶")
        else:
            self.settings_panel.setText("⚙ Settings    ▼")

    def unfold_basic_parameters(self):
        self.settings_window = BasicParameters(self)
        self.settings_window.show()

    def unfold_visual_display(self):
        self.settings_window = VisualDisplay(self)
        self.settings_window.show()

    def unfold_cannon_settings(self):
        self.settings_window = CannonSettings(self)
        self.settings_window.show()

    def unfold_cannonball_details(self):
        self.settings_window = CannonballDetails(self)
        self.settings_window.show()

    def change_air_density_size(self,value):
        print("air density:", value)

    def change_gravity_size(self,value):
        print("gravity:", value)

    def change_initial_velocity_size(self, value):
        print("Initial velocity:", value)

    def change_cannonball_mass_size(self, value):
        print("Cannonball mass:", value)

    def change_cannon_height_size(self, value):
        print("Cannon height:", value)

    def change_cannonball_radius_size(self, value):
        print("Cannonball radius:", value)

    def change_firing_angle_size(self, value):
        print("Firing angle:", value)

    def paintEvent(self, event):
        painter = QPainter(self)
        scaled = self.background.scaled(self.size(), aspectRatioMode=2)
        painter.drawPixmap(0, 0, scaled)




app = QApplication(sys.argv)
window = Program()
window.show()
sys.exit(app.exec_())