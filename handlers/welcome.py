from handlers.window_base import WindowBase
from handlers.organization_add import OrganizationAdd
from handlers.search import Search
from PyQt6.QtWidgets import QDialog, QMainWindow
from ui_models.welcome_window_design import Ui_welcome_window
from ui_models.organization_add_design import Ui_MainWindow
from ui_models.search_window_design import Ui_search_window


class Welcome(WindowBase):
    def __init__(self, name, window:QDialog, ui:Ui_welcome_window):
        super().__init__(name, window, ui)

        self.ui.search_btn.clicked.connect(self.open_search_organizations)
        self.ui.add_btn.clicked.connect(self.open_add_organizations)

    def open_search_organizations(self):
        search = Search("search", QDialog(), Ui_search_window())
        search.open()

    def open_add_organizations(self):
        add = OrganizationAdd("add organization", QMainWindow(), Ui_MainWindow())
        add.open()
