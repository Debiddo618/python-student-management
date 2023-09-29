import sys

from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QLineEdit, QGridLayout, QComboBox


class Calculator(QWidget):
    def __init__(self):
        super().__init__()
        # set the title of the window
        self.setWindowTitle("Average Speed Calculator")

        grid = QGridLayout()

        distance = QLabel("Distance")
        self.distance_line_edit = QLineEdit()

        time = QLabel("Time (hours)")
        self.time_line_edit = QLineEdit()

        self.metric = QComboBox()
        self.metric.addItems(["Metric (km)", "Imperial (miles)"])

        self.output = QLabel("")

        calculate = QPushButton("Calculate")
        calculate.clicked.connect(self.calculate_speed)

        grid.addWidget(distance, 0, 0)
        grid.addWidget(self.distance_line_edit, 0, 1)
        grid.addWidget(self.metric, 0, 3)
        grid.addWidget(time, 1, 0)
        grid.addWidget(self.time_line_edit, 1, 1)
        grid.addWidget(calculate, 2, 1)
        grid.addWidget(self.output,3,0,1,3)

        self.setLayout(grid)

    def calculate_speed(self):
        distance = self.distance_line_edit.text()
        time = self.time_line_edit.text()
        metric = self.metric.currentText()
        if metric == "Metric (km)":
            unit = "km/h"
        else:
            unit = "mhp"
        print(metric)
        average_speed = "Average Speed: {} {}".format(int(distance) / int(time),unit)
        self.output.setText(average_speed)

# This is the same for all applications
app = QApplication(sys.argv)
speed_calculator = Calculator()
speed_calculator.show()
sys.exit(app.exec())
