import sys
from PyQt6.QtCore import Qt
import sqlite3
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtWidgets import (QApplication, QLabel, QPushButton, QLineEdit, QGridLayout, QComboBox, QMainWindow,
                             QTableWidget, QTableWidgetItem, QDialog, QVBoxLayout, QToolBar, QStatusBar, QMessageBox)


class DatabaseConnection:
    def __init__(self, database="database.db"):
        self.database_file = database

    def connect(self):
        connection = sqlite3.connect(self.database_file)
        return connection


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Management System")
        self.setMinimumSize(800, 600)

        # create menu items
        file_menu_item = self.menuBar().addMenu("&File")
        help_menu_item = self.menuBar().addMenu("&Help")
        edit_menu_item = self.menuBar().addMenu("&Edit")

        # add sub-items for each menu item
        add_student_action = QAction(QIcon("icons/add.png"), "Add Student", self)
        add_student_action.triggered.connect(self.insert)
        file_menu_item.addAction(add_student_action)

        about_action = QAction("About", self)
        help_menu_item.addAction(about_action)
        # this line is needed, otherwise the about menu item will not show
        about_action.setMenuRole(QAction.MenuRole.NoRole)
        about_action.triggered.connect(self.about)

        search_action = QAction(QIcon("icons/search.png"), "Search", self)
        search_action.triggered.connect(self.search)
        edit_menu_item.addAction(search_action)

        # create table
        self.table = QTableWidget()

        # setting 4 columns
        self.table.setColumnCount(4)
        # labeling every column
        self.table.setHorizontalHeaderLabels(("Id", "Name", "Course", "Mobile"))
        # removing the default index
        self.table.verticalHeader().setVisible(False)
        # adding the table to the window
        self.setCentralWidget(self.table)

        # Creating a toolbar and add toolbar elements
        toolbar = QToolBar()
        toolbar.setMovable(True)
        self.addToolBar(toolbar)
        toolbar.addAction(add_student_action)
        toolbar.addAction(search_action)

        # create status bar and add status bar elements
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        # detect a cell click
        self.table.cellClicked.connect(self.cell_clicked)

    def cell_clicked(self):
        edit_button = QPushButton("Edit Record")
        edit_button.clicked.connect(self.edit)

        delete_button = QPushButton("Delete Record")
        delete_button.clicked.connect(self.delete)

        children = self.findChildren(QPushButton)
        if children:
            for child in children:
                self.status_bar.removeWidget(child)

        self.status_bar.addWidget(edit_button)
        self.status_bar.addWidget(delete_button)

    def load_data(self):
        # connecting to the database
        connection = DatabaseConnection().connect()
        # making a query
        result = connection.execute("SELECT * FROM students")
        # print(result)

        # this line prevent duplicate
        self.table.setRowCount(0)

        # loading the data
        for row_number, row_data in enumerate(result):
            # inserting an empty row
            self.table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                # populating every cell with the data
                self.table.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        connection.close()

    def insert(self):
        dialog = InsertDialog()
        dialog.exec()

    def search(self):
        dialog = SearchDialog()
        dialog.exec()

    def about(self):
        dialog = AboutDialog()
        dialog.exec()

    def edit(self):
        dialog = EditDialog()
        dialog.exec()

    def delete(self):
        dialog = DeleteDialog()
        dialog.exec()


class AboutDialog(QMessageBox):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("About")
        content = """
        This app was created during the course "The Python Mega Course".
        Feel Free to modify and reuse this app
        """
        self.setText(content)


class DeleteDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Delete Student Data")

        layout = QGridLayout()
        confirmation = QLabel("Are you sure you want to delete?")
        yes = QPushButton("Yes")
        no = QPushButton("No")
        layout.addWidget(confirmation, 0, 0, 1, 2)
        layout.addWidget(yes, 1, 0)
        layout.addWidget(no, 1, 1)
        self.setLayout(layout)

        # getting the id of the student
        index = main_window.table.currentRow()
        self.student_id = main_window.table.item(index, 0)

        yes.clicked.connect(self.delete_student)
        no.clicked.connect(self.close)

    def delete_student(self):
        connection = DatabaseConnection().connect()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM students WHERE id = ?", (self.student_id.text(),))
        connection.commit()
        cursor.close()
        connection.close()
        main_window.load_data()
        self.close()
        confirmation_widget = QMessageBox()
        confirmation_widget.setWindowTitle("Success")
        confirmation_widget.setText("The record was deleted successfully")
        confirmation_widget.exec()


class EditDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Update Student Data")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()

        # getting the student name of the selected column
        index = main_window.table.currentRow()
        student_name = main_window.table.item(index, 1).text()

        # Getting the id of the student
        self.student_id = main_window.table.item(index, 0)

        # add student name widget
        self.student_name = QLineEdit(student_name)
        self.student_name.setPlaceholderText("Name")
        layout.addWidget(self.student_name)

        # getting the current value of the combobox
        course = main_window.table.item(index, 2).text()

        # add course combo box
        self.course_name = QComboBox()
        self.course_name.addItems(["Biology", "Math", "Astronomy", "Physics"])
        self.course_name.setCurrentText(course)
        layout.addWidget(self.course_name)

        # getting the value of the mobile number
        mobile = main_window.table.item(index, 3).text()

        # add phone number widget
        self.mobile = QLineEdit(mobile)
        self.mobile.setPlaceholderText("Mobile")
        layout.addWidget(self.mobile)

        # add a submit button
        submit = QPushButton("Update")
        submit.clicked.connect(self.update_student)
        layout.addWidget(submit)

        self.setLayout(layout)

    def update_student(self):
        student_name = self.student_name.text()
        course_name = self.course_name.currentText()
        mobile = self.mobile.text()
        student_id = self.student_id.text()

        connection = DatabaseConnection().connect()
        cursor = connection.cursor()
        cursor.execute("UPDATE students SET name = ?, course = ?, mobile = ? WHERE id = ?",
                       (student_name, course_name, mobile, student_id))
        connection.commit()
        cursor.close()
        connection.close()
        main_window.load_data()
        self.close()

        confirmation_widget = QMessageBox()
        confirmation_widget.setWindowTitle("Success")
        confirmation_widget.setText("The record was updated successfully")
        confirmation_widget.exec()


class SearchDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Search Student")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()

        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("Name")

        search = QPushButton("Search")
        search.clicked.connect(self.search)

        layout.addWidget(self.student_name)
        layout.addWidget(search)

        self.setLayout(layout)

    def search(self):
        student_name = self.student_name.text()
        main_window.table.clearSelection()
        items = main_window.table.findItems(student_name, Qt.MatchFlag.MatchFixedString)
        for item in items:
            main_window.table.item(item.row(), 1).setSelected(True)
        self.close()


class InsertDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Insert Student Data")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()

        # add student name widget
        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("Name")
        layout.addWidget(self.student_name)

        # add course combo box
        self.course_name = QComboBox()
        self.course_name.addItems(["Biology", "Math", "Astronomy", "Physics"])
        layout.addWidget(self.course_name)

        # add phone number widget
        self.mobile = QLineEdit()
        self.mobile.setPlaceholderText("Mobile")
        layout.addWidget(self.mobile)

        # add a submit button
        submit = QPushButton("Register")
        submit.clicked.connect(self.add_student)
        layout.addWidget(submit)

        self.setLayout(layout)

    def add_student(self):
        name = self.student_name.text()
        course = self.course_name.currentText()
        mobile = self.mobile.text()
        connection = DatabaseConnection().connect()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO students (name, course, mobile) VALUES(?,?,?)",
                       (name, course, mobile))
        connection.commit()
        cursor.close()
        connection.close()
        main_window.load_data()
        self.close()

        confirmation_widget = QMessageBox()
        confirmation_widget.setWindowTitle("Success")
        confirmation_widget.setText("The record was added successfully")
        confirmation_widget.exec()


# This is the same for all applications
app = QApplication(sys.argv)
main_window = MainWindow()
main_window.show()
main_window.load_data()
sys.exit(app.exec())
