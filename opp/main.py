import typing
from PyQt6 import QtCore
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QTextEdit, QPushButton, QVBoxLayout, QWidget
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QTextEdit, QPushButton, QVBoxLayout, QWidget, QTableWidget, QTableWidgetItem, QComboBox

import pattern_ch

class Car:
    def __init__(self, name, manufacturer,
                 model_range, color, engine_type):
        self.num = name
        self.manufacturer = manufacturer
        self.model_range = model_range
        self.color = color
        self.engine_type = engine_type


class AddWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Adding car")
        self.setFixedSize(QSize(300, 500))

        layout = QVBoxLayout()
        central_widget = QWidget()

        self.info = []
        self.input_fields = []

        for i_spec in pattern_ch.info_pattern:
            self.name_label = QLabel(f"{i_spec}*:")
            if isinstance(pattern_ch.info_pattern[i_spec], list):
                self.name_input = QComboBox()
                self.name_input.addItems(pattern_ch.info_pattern[i_spec])
            else:
                self.name_input = QLineEdit()
                if i_spec == "Номер машины":
                    self.name_input.textChanged.connect(self.validate_num)
                elif i_spec == "Цвет" or i_spec == "Производитель":
                    self.name_input.textChanged.connect(self.validate_text)
                else:
                     self.name_input.textChanged.connect(self.validate)
                self.name_input.returnPressed.connect(self.move_focus)

            layout.addWidget(self.name_label)
            layout.addWidget(self.name_input)

            self.info.append(self.name_input)
            self.input_fields.append(self.name_input)

            central_widget.setLayout(layout)
            self.setCentralWidget(central_widget)

        self.save_button = QPushButton("Сохранить")
        self.save_button.clicked.connect(self.save_info)
        layout.addWidget(self.save_button)

        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    # перемещает фокус на след строку
    def move_focus(self):
        current_index = -1
        for index, input_field in enumerate(self.input_fields):
            if input_field.hasFocus():
                current_index = index
                break
        next_index = (current_index + 1) % len(self.input_fields)
        self.input_fields[next_index].setFocus()


    # проверки
    def validate(self, text):
        input_field = self.sender()
        if text == "":
            input_field.setStyleSheet("QLineEdit { background-color: rgb(255, 200, 200); }")
        else:
            input_field.setStyleSheet("QLineEdit { background-color: white; }")

    def validate_num(self, text):
        input_field = self.sender()
        try:
            if len(text) >= 8\
                and text[0] in 'АВЕКМНОРСТУХ' and (0 <= int(text[1:4]) < 1000)\
                and text[4] in 'АВЕКМНОРСТУХ'\
                and text[5] in 'АВЕКМНОРСТУХ'and (0 <= int(text[-2:]) < 1000):
             input_field.setStyleSheet("QLineEdit { background-color: white; }")
            else:
                raise Exception
        except Exception:
            input_field.setStyleSheet("QLineEdit { background-color: rgb(255, 200, 200); }")

    def validate_text(self, text):
        input_field = self.sender()
        if text.isalpha():
            input_field.setStyleSheet("QLineEdit { background-color: white; }")
        else:
             input_field.setStyleSheet("QLineEdit { background-color: rgb(255, 200, 200); }")


    def save_info(self):
        saved_info = []
        for input_field in self.info:
            text = input_field.currentText() if isinstance(input_field, QComboBox) else input_field.text()
            saved_info.append(text)

        with open("cars.txt", "a", encoding = "UTF-8") as file:
            file.write("\n".join(saved_info) + "\nend\n")

        print(saved_info)



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Car Accounting")

        self.setFixedSize(QSize(300, 200))

        self.add_button = QPushButton("Добавить")
        self.delete_button = QPushButton("Удалить")
        self.search_button = QPushButton("Найти")
        self.all_machines_button = QPushButton("Список машин")

        layout = QVBoxLayout()
        layout.addWidget(self.add_button)
        layout.addWidget(self.delete_button)
        layout.addWidget(self.search_button)
        layout.addWidget(self.all_machines_button)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.add_button.clicked.connect(self.adding)
        self.delete_button.clicked.connect(self.delete_machine)
        self.search_button.clicked.connect(self.search_machines)
        self.all_machines_button.clicked.connect(self.show_all_machines)

    def show_all_machines(self):
        pass
        # all_machines_window = AllMachinesWindow(self.machines)
        # all_machines_window.show()

    def adding(self):
        self.adding_window = AddWindow()
        self.adding_window.show()
        # self.machines.append(machine)

    def delete_machine(self):
        machine_name = self.machine_name_input.text()
        # TODO: Add code to delete machine details from the text file database
        pass

    def sort_machines(self):
        # TODO: Add code to sort machines in the text file database
        pass

    def search_machines(self):
        search_term = self.machine_name_input.text()
        # TODO: Add code to search for machines in the text file database
        pass

# Create the application instance and main window
app = QApplication([])
window = MainWindow()
window.show()
app.exec()
