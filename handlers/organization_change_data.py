from database.database import DataBase
from handlers.organization_add import OrganizationAdd
from handlers.data import OrganizationData
from handlers.data_preprocessor import DataPreprocessor
from PyQt6.QtWidgets import QMainWindow
from ui_models.organization_change_data_design import Ui_MainWindow

class OrganizationDataChange(OrganizationAdd):
    def __init__(self, name, window:QMainWindow, ui:Ui_MainWindow):
        super().__init__(name, window, ui)
        self.data = None
        self.ui.final_btn.disconnect()
        self.ui.final_btn.clicked.connect(self.close)

    def set_values(self):
        self.ui.full_name_input.setText(self.data.full_name)
        self.ui.name_input.setText(self.data.short_name)
        self.ui.address_input.setText(self.data.address)
        self.ui.email_input.setText(self.data.email)
        self.update_person_table()
        self.update_phone_table()

    def open(self, data:OrganizationData):
        self.data = data
        self.set_values()
        super().open()

        
    def close(self):
        self.collect_data()
        if self.data.validate():
            DataBase.update_data(self.data)
        super().close()

    