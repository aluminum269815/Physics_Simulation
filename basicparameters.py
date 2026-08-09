from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class BasicParameters(QWidget):

    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setWindowTitle("Basic Parameters")
        self.setFixedSize(350, 250)
        self.setStyleSheet("""
            QLabel{
                font-family: Arial;
            }
        
        """)

        air_resistance_label = QLabel("Air resistance")

        self.air_resistance_checkbox = QCheckBox()

        air_density_label= QLabel("Air Density")

        self.air_density_slider = QSlider(Qt.Horizontal)
        self.air_density_slider.setMinimum(0)
        self.air_density_slider.setMaximum(100000)
        self.air_density_slider.setValue(1225)

        self.air_density_input = QLineEdit()
        self.air_density_input.setText("1.225")
        self.air_density_input.setFixedWidth(60)
        air_density_unit_label = QLabel("kg/m<sup>-3<sup>")

        self.air_density_input.editingFinished.connect(self.change_air_density)
        self.air_density_slider.valueChanged.connect(self.update_air_density)

        gravity_label = QLabel("Gravity(Downward acceleration)")

        self.gravity_slider = QSlider(Qt.Horizontal)
        self.gravity_slider.setMinimum(0)
        self.gravity_slider.setMaximum(60000)
        self.gravity_slider.setValue(9810)

        self.gravity_input = QLineEdit()
        self.gravity_input.setText("9.81")
        self.gravity_input.setFixedWidth(60)
        gravity_unit_label = QLabel("m/s<sup>-2<sup> ")

        self.gravity_input.editingFinished.connect(self.change_gravity)
        self.gravity_slider.valueChanged.connect(self.update_gravity)

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

    def update_air_density(self, value):
        air_density = value / 1000
        self.air_density_input.setText(f"{air_density:.3f}")
        self.main_window.change_air_density_size(air_density)

    def change_air_density(self):
        try:
            value = float(self.air_density_input.text())
            slider_value = int(value * 1000)
            self.air_density_slider.setValue(slider_value)
        except ValueError:
            pass

    def update_gravity(self, value):
        gravity = value / 1000
        self.gravity_input.setText(f"{gravity:.3f}")
        self.main_window.change_gravity_size(gravity)


    def change_gravity(self):
        try:
            value = float(self.gravity_input.text())
            slider_value = int(value * 1000)
            self.gravity_slider.setValue(slider_value)
        except ValueError:
            pass