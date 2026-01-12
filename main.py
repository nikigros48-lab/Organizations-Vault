from PyQt6.QtWidgets import QApplication, QDialog
from handlers.welcome import Welcome
from ui_models.welcome_window_design import Ui_welcome_window


app = QApplication([])

welcome_window = Welcome("welcome", QDialog(), Ui_welcome_window())


welcome_window.window.open()

app.exec()