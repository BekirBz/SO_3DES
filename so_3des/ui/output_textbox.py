from PyQt5.QtCore import Qt, QTextStream, QBuffer, QByteArray
from PyQt5.QtGui import QFont, QKeySequence
from PyQt5.QtWidgets import *

class OutputTextBox(QPlainTextEdit):
    def __init__(self, parent, size = None, font_size = 16, font_color = "red"):
        super().__init__(parent)
        self.font_color = font_color
        self._placeholder_text = ""
        # set size
        if size:
            self.setFixedSize(size[0], size[1])

        # set font size
        default_font = QFont()
        default_font.setPointSize(font_size)
        self.setFont(default_font)

        self.setStyleSheet(f"color: {self.font_color};")

        # enable word wrapping
        self.setWordWrapMode(True)
        self.setLineWrapMode(True)
        self.setReadOnly(True)

        # Scroll Bar
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

    def update_text(self, output_text):
        """ Replaces all text in the text box with the new text"""
        self.reset()
        self.clearFocus()
        self.setPlainText(output_text)


    def get_text(self):
        return self.toPlainText()

    def reset(self):
        """ reset text box to default, clear text box, show default text"""
        self.clear()

