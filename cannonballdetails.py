from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class CannonballDetails(QWidget):

    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setWindowTitle("Cannonball Details")
        self.setFixedSize(550, 400)
        self.setStyleSheet("font-family: Arial;")


        cannonball_title_label = QLabel("Cannonball Details")
        cannonball_mass_info = QLabel("Cannonball Mass:__kg")
        cannonball_radius_info = QLabel("Cannonball Radius:__cm")

        v_title_label = QLabel("Velocity")
        v_hori_info = QLabel("v<sub>horizontal</sub>:__m/s<sup>-1</sup>")
        v_vert_info = QLabel("v<sub>vertical</sub>:__m/s<sup>-1<sup>")
        v_total_info = QLabel("v<sub>total</sub>:__m/s<sup>-1</sup>")

        a_title_label = QLabel("Acceleration")
        a_hori_info = QLabel("a<sub>horizontal</sub>:__m/s<sup>-2</sup>")
        a_vert_info = QLabel("a<sub>vertical</sub>:__m/s<sup>-2</sup>")
        a_total_info = QLabel("a<sub>total</sub>:__m/s<sup>-2</sup>")

        e_title_label = QLabel("Energy")
        ke_info = QLabel("Kinetic Energy:__j")
        gpe_info = QLabel("Gravitational Potential Energy:__j")

        posi_title_label = QLabel("Position")
        posi_hori_info = QLabel("Horizontal:__m")
        posi_vert_info = QLabel("Vertical:__m")

        layout = QVBoxLayout()

        layout.addStretch()


        row1 = QHBoxLayout()
        row1.addStretch(1)
        row1.addWidget(cannonball_title_label)
        row1.addStretch(3)

        layout.addLayout(row1)
        layout.addWidget(cannonball_mass_info, alignment=Qt.AlignHCenter)
        layout.addWidget(cannonball_radius_info, alignment=Qt.AlignHCenter)

        row2 = QHBoxLayout()
        row2.addStretch(1)
        row2.addWidget(v_title_label)
        row2.addStretch(3)

        layout.addLayout(row2)
        layout.addWidget(v_hori_info, alignment=Qt.AlignHCenter)
        layout.addWidget(v_vert_info, alignment=Qt.AlignHCenter)
        layout.addWidget(v_total_info, alignment=Qt.AlignHCenter)

        row3 = QHBoxLayout()
        row3.addStretch(1)
        row3.addWidget(a_title_label)
        row3.addStretch(3)

        layout.addLayout(row3)
        layout.addWidget(a_hori_info, alignment=Qt.AlignHCenter)
        layout.addWidget(a_vert_info, alignment=Qt.AlignHCenter)
        layout.addWidget(a_total_info, alignment=Qt.AlignHCenter)


        row4 = QHBoxLayout()
        row4.addStretch(1)
        row4.addWidget(e_title_label)
        row4.addStretch(3)

        layout.addLayout(row4)
        layout.addWidget(ke_info, alignment=Qt.AlignHCenter)
        layout.addWidget(gpe_info, alignment=Qt.AlignHCenter)

        row5 = QHBoxLayout()
        row5.addStretch(1)
        row5.addWidget(posi_title_label)
        row5.addStretch(3)

        layout.addLayout(row5)
        layout.addWidget(posi_hori_info, alignment=Qt.AlignHCenter)
        layout.addWidget(posi_vert_info, alignment=Qt.AlignHCenter)

        layout.addStretch()

        self.setLayout(layout)