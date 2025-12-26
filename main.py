from database.database import DataBase
from handlers.welcome import Welcome
from PyQt6.QtWidgets import QApplication, QDialog
from ui_models.welcome_window_design import Ui_welcome_window


app = QApplication([])

DataBase.create_database()
welcome_window = Welcome("welcome", QDialog(), Ui_welcome_window())

welcome_window.window.open()

app.exec()