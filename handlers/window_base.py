class WindowBase:
    windows = {}

    def __init__(self, name, window, ui):
        self.window = window
        self.ui = ui
        self.ui.setupUi(window)
        WindowBase.windows[name] = self

    def open(self):
        self.window.show()

    def close(self):
        self.window.close()
        