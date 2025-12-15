from handlers.window_base import WindowBase
from handlers.data import OrganizationData
from handlers.person_form import PersonForm
from handlers.data_preprocessor import DataPreprocessor
from handlers.database import DataBase
from handlers.person_form import PersonForm
from PyQt6.QtWidgets import QMainWindow, QMessageBox, QTableWidgetItem, QPushButton
from PyQt6.QtCore import QRegularExpression
from PyQt6.QtGui import QRegularExpressionValidator
from ui_models.organization_add_design import Ui_MainWindow
from ui_models.person_form_design import Ui_Dialog


class OrganizationAdd(WindowBase):

    
    def __init__(self, name, window:QMainWindow, ui:Ui_MainWindow):
        super().__init__(name, window, ui)
        self.data = OrganizationData()
        
        phone_validator = QRegularExpressionValidator(QRegularExpression(r"[0-9]{5,11}"))
        self.ui.phone_input.setValidator(phone_validator)
        self.ui.phone_input.setMaxLength(11)
        self.ui.phone_table.setColumnWidth(0, 600)
        self.ui.phone_table.setColumnWidth(1, 100)
        self.ui.phone_input.setPlaceholderText("89...")

        self.ui.phone_add_btn.clicked.connect(self.append_phone)
        self.ui.person_add_btn.clicked.connect(self.append_contact)
        self.ui.back_btn.clicked.connect(self.close)
        self.ui.final_btn.clicked.connect(self.organization_record)
    
    def collect_data(self):
        self.data.full_name = self.ui.full_name_input.text()
        self.data.short_name = self.ui.name_input.text()
        self.data.address = self.ui.address_input.text()

    def append_phone(self):
        phone_number = self.ui.phone_input.text().strip()
        if phone_number != "":
            if phone_number not in self.data.phones:
                self.data.phones.append(phone_number)
                self.ui.phone_input.setText("")
                self.update_phone_table()
            else:
                QMessageBox.warning(self.window, "Ошибка!", "Такой номер уже существует")
        else:
            QMessageBox.warning(self.window, "Ошибка!", "Поле с номером пустое!")  

    def update_phone_table(self):
        self.ui.phone_table.clearContents()
        self.ui.phone_table.setRowCount(len(self.data.phones))
        self.ui.phone_table.setColumnCount(2)
        for row, phone in enumerate(self.data.phones):
            item = QTableWidgetItem(phone)
            self.ui.phone_table.setItem(row, 0, item)
            delete_button = QPushButton("Удалить")
            delete_button.clicked.connect(lambda _, r=row: self.delete_phone(r))
            self.ui.phone_table.setCellWidget(row, 1, delete_button)

    def delete_phone(self, row):
        phone_to_delete = self.ui.phone_table.item(row, 0).text()
        self.data.phones.remove(phone_to_delete)
        self.update_phone_table()

    def append_contact(self):
        contact = PersonForm(self.window, Ui_Dialog)
        result = contact.exec()
        if bool(result) == True:
            self.data.contacts.append(contact.data)
            self.update_person_table()

    def update_person_table(self):
        self.ui.persons_table.clearContents()
        self.ui.persons_table.setRowCount(len(self.data.contacts))
        self.ui.persons_table.setColumnCount(3)
        
        for row, contact in enumerate(self.data.contacts):
            item = QTableWidgetItem(contact.name)
            self.ui.persons_table.setItem(row, 0, item)
            delete_btn = QPushButton("Удалить")
            delete_btn.clicked.connect(lambda _, r=row: self.delete_contact(r))
            self.ui.persons_table.setCellWidget(row, 1, delete_btn)
            change_btn = QPushButton("Изменить")
            change_btn.clicked.connect(lambda _, r=row: self.change_contact(r))
            self.ui.persons_table.setCellWidget(row, 2, change_btn)

    def delete_contact(self, row):
        contact_to_delete = self.ui.persons_table.item(row, 0).text()
        found_contact = next(contact for contact in self.data.contacts if contact.name == contact_to_delete)
        self.data.contacts.remove(found_contact)
        self.update_person_table()

    def change_contact(self, row):
        contact_to_change = self.ui.persons_table.item(row, 0).text()
        found_contact = next(contact for contact in self.data.contacts if contact.name == contact_to_change)
        form = PersonForm(self.window, Ui_Dialog)
        form.open(found_contact)
        result = form.exec()
        if bool(result) == True:
            self.update_person_table()

    def organization_record(self):
        self.collect_data()
        if self.data.validate():
            prepare_data = DataPreprocessor.prepare_data(self.data)
            DataBase.insert_data(prepare_data)
            QMessageBox.information(self.window, "Успех!", "Организация добавлена!")
            self.close()
        else:
            QMessageBox.warning(self.window, "Ошибка!", "Заполните все поля!")