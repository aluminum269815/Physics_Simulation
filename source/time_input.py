from PyQt5.QtWidgets import QLineEdit
from PyQt5.Qt import Qt


class TimeInput(QLineEdit):
    def __init__(self, program):
        super().__init__(program)
        self.program = program
        self.settings = self.program.settings

        self.setFixedSize(250, 60)
        self.setText('0.00 / 0.00')
        self.setAlignment(Qt.AlignHCenter)
        self.setStyleSheet('font-size: 30px')
        self.setEnabled(False)
        self.editingFinished.connect(self.change_time)

    def update_value(self):
        self.setText(f'{self.settings.time:.2f} / {self.settings.max_time:.2f}')
        self.setEnabled(self.settings.max_time > 0)

    def change_time(self):
        try:
            time = round(float(self.text()), 2)
            self.program.change_time(time)
        except ValueError:
            self.update_value()

    def focusInEvent(self, event):
        self.program.pause()
        self.setText(f'{self.settings.time: .2f}')
        super().focusInEvent(event)
