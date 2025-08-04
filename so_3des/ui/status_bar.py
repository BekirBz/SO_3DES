from PyQt5.QtWidgets import QStatusBar

class StatusBar(QStatusBar):
    def __init__(self, parent, default_text = ""):
        super().__init__(parent)
        self.showMessage(default_text)
        # attach to QMainWindow
        parent.setStatusBar(self)

    def update_status_bar(self, text):
        self.showMessage(text)
        self.update()