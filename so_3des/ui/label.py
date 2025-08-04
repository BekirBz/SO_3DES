from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import *

class Label(QLabel):
    def __init__(self, parent, text = "", font_size = int):
        super().__init__(parent)
        self.setText(text)

        # set font size
        default_font = QFont()
        default_font.setPointSize(font_size)
        self.setFont(default_font)

        # make the text wrap within the widget
        self.setWordWrap(True)
