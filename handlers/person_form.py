from PyQt6.QtWidgets import QDialog, QMessageBox, QTableWidgetItem, QPushButton
from PyQt6.QtCore import QRegularExpression
from PyQt6.QtGui import QRegularExpressionValidator
from handlers.person_data import Person

class PersonForm(QDialog):
    def __init__(self, parent=None, ui_class=None):
        super().__init__(parent)
        self.ui = ui_class()
        self.ui.setupUi(self)
        self.data = Person()
        
        phone_validator = QRegularExpressionValidator(QRegularExpression(r"[0-9]{5,11}"))
        self.ui.phone_input.setValidator(phone_validator)
        self.ui.phone_input.setMaxLength(11)
        self.ui.phone_input.setPlaceholderText("89...")
        self.ui.phone_add_btn.clicked.connect(self.append_phone)
        self.ui.ok_btn.clicked.connect(self.collect_data)
        self.ui.cancel_btn.clicked.connect(self.reject)

    def collect_data(self):
        self.data.name = self.ui.name_input.text()
        self.data.post = self.ui.post_input.text()
        self.data.email = self.ui.email_input.text()
        if self.data.validation():
            self.accept()
        else:
            QMessageBox.warning(self, "Ошибка!", "Заполните все необходимые поля!")

    def append_phone(self):
        phone_number = self.ui.phone_input.text().strip()
        if phone_number != "":
            if phone_number not in self.data.phones:
                self.data.phones.append(phone_number)
                self.ui.phone_input.setText("")
                self.update_phone_table()
            else:
                QMessageBox.warning(self, "Ошибка!", "Такой номер уже существует")
        else:
            QMessageBox.warning(self, "Ошибка!", "Поле с номером пустое!")
    
    def update_phone_table(self):
        self.ui.numbers_table.clearContents()
        self.ui.numbers_table.setRowCount(len(self.data.phones))
        self.ui.numbers_table.setColumnCount(2)
        for row, phone in enumerate(self.data.phones):
            item = QTableWidgetItem(phone)
            self.ui.numbers_table.setItem(row, 0, item)
            delete_button = QPushButton("Удалить")
            delete_button.clicked.connect(lambda _, r=row: self.delete_phone(r))
            self.ui.numbers_table.setCellWidget(row, 1, delete_button)

    def delete_phone(self, row):
        phone_to_delete = self.ui.numbers_table.item(row, 0).text()
        self.data.phones.remove(phone_to_delete)
        self.update_phone_table()

    def set_values(self):
        self.ui.name_input.setText(self.data.name)
        self.ui.post_input.setText(self.data.post)
        self.ui.email_input.setText(self.data.email)
        self.update_phone_table()

    def open(self, data=None):
        if data is not None:
            self.data = data
            self.set_values()
        super().open()