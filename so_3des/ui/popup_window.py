from PyQt5.QtWidgets import QMessageBox

class PopUpWindow:
    def __init__(self):
        pass

    def show_warning_popup(self, title, message):
        """ Showing warning message. """
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec_()