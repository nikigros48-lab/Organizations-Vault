from handlers.window_base import WindowBase
from handlers.database import DataBase
from handlers.data_preprocessor import DataPreprocessor
from handlers.organization_change_data import OrganizationDataChange
from PyQt6.QtWidgets import QDialog, QTableWidgetItem, QPushButton, QMainWindow
from ui_models.search_window_design import Ui_search_window
from ui_models.organization_change_data_design import Ui_MainWindow


class Search(WindowBase):
    def __init__(self, name, window:QDialog, ui:Ui_search_window):
        super().__init__(name, window, ui)
        self.data = None
        self.ui.search_table.setColumnWidth(0, 320)
        self.ui.search_table.setColumnWidth(1, 80)
        self.ui.search_btn.clicked.connect(self.search)

    def search(self):
        search_query = self.ui.search_input.text()
        if search_query != "":
            self.data = DataPreprocessor.transform_record_to_objects(DataBase.search_data(search_query))
            self.update_search_table()
            

    def update_search_table(self):
        self.ui.search_table.clearContents()
        self.ui.search_table.setRowCount(len(self.data))
        self.ui.search_table.setColumnCount(2)
        if self.data is not None:
            for row, organization in enumerate(self.data):
                item = QTableWidgetItem(organization.short_name)
                self.ui.search_table.setItem(row, 0, item)
                change_btn = QPushButton("Изменить")
                change_btn.clicked.connect(lambda _, r=row: self.change_organization_data(r))
                self.ui.search_table.setCellWidget(row, 1, change_btn)


    def change_organization_data(self, row):
        organization_to_change = self.ui.search_table.item(row, 0).text()
        found_organization_data = next(organization for organization in self.data if organization.short_name == organization_to_change)
        change_organization = OrganizationDataChange("change organization", QMainWindow(), Ui_MainWindow())
        change_organization.open(found_organization_data)
    