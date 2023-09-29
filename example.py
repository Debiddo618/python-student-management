import sys
from datetime import datetime
from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QGridLayout, QLineEdit, QPushButton


# QWidget is a class that creates the window
class AgeCalculator(QWidget):
    def __init__(self):
        # need to call the init method of the parent class. Else: error
        super().__init__()

        # add a title
        self.setWindowTitle("Age Calculator")

        # create the widgets
        grid = QGridLayout()
        name_label = QLabel("Name: ")
        self.name_line_edit = QLineEdit()
        date_label = QLabel("Date of Birth MM/DD/YYYY")
        self.date_line_edit = QLineEdit()
        calculate_button = QPushButton("Calculate Age")
        calculate_button.clicked.connect(self.calculate_age)
        self.output_label = QLabel("")

        # adding widgets to the grid layout [row,column,how many rows, and how many columns]
        grid.addWidget(name_label,0,0)
        grid.addWidget(self.name_line_edit,0,1)
        grid.addWidget(date_label,1,0)
        grid.addWidget(self.date_line_edit,1,1)

        # buttton on [2,0], 1 row and 2 columns
        grid.addWidget(calculate_button,2,0,1,2)
        grid.addWidget(self.output_label,3,0,1,2)

        # setting the grid layout
        self.setLayout(grid)
    def calculate_age(self):
        current_year = datetime.now().year
        date_birth_year = self.date_line_edit.text()
        year_of_birth = datetime.strptime(date_birth_year,"%m/%d/%Y").date().year
        age = current_year-year_of_birth
        self.output_label.setText("{} is {} years old.".format(self.name_line_edit.text(),age))


# app must be instantiated
app = QApplication(sys.argv)
age_calculator = AgeCalculator()
age_calculator.show()
sys.exit(app.exec())