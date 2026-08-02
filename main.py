import os, sys

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from settings import Settings
from basicparameters import BasicParameters

class Program:
def **init**(self):
self.settings = Settings()
self.app = QApplication(sys.argv)
self.window = Window()

```
def run(self):
    self.window.show()
    sys.exit(self.app.exec_())
```

class Window(QWidget):
def **init**(self):
super().**init**()

```
    self.setWindowTitle("Projectile Motion sim")
    self.background = QPixmap(os.path.abspath("asset/background.png"))
    self.resize(800, 500)

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

    self.basic_parameters_button.clicked.connect(self.unfold_settings_panel)

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

def unfold_settings_panel(self):
    self.settings_window = BasicParameters(self)
    self.settings_window.show()

def change_air_density_size(self, value):
    print("Air density:", value)

def change_gravity_size(self, value):
    print("Gravity:", value)

def paintEvent(self, event):
    painter = QPainter(self)
    scaled = self.background.scaled(self.size(), aspectRatioMode=2)
    painter.drawPixmap(0, 0, scaled)

program = Program()
program.run()
