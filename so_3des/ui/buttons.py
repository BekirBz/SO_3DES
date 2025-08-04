from PyQt5.QtWidgets import *

class Button(QPushButton):
    def __init__(self, parent, size, button_text = str, on_button_click = None ):
        super().__init__(button_text, parent)
        if size:
            self.setFixedSize(size[0], size[1])
        if on_button_click:
            self.clicked.connect(on_button_click)