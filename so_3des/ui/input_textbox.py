import base64
import os
import re

from PyQt5.QtGui import QFont, QKeySequence
from PyQt5.QtWidgets import *
from charset_normalizer import is_binary


def is_binary(binary_str):
    # Check if the string consists only of '0' and '1' and is a multiple of 8 in length
    return bool(re.match('^[01]+$', binary_str)) and len(binary_str) % 8 == 0
def is_hexadecimal(s):
    # Check if the string contains only valid hexadecimal characters (0-9, a-f, A-F)
    return bool(re.match('^[0-9a-fA-F]+$', s))
def hex_to_bin(hex_str):
    # Convert hex to an integer
    decimal_value = int(hex_str, 16)
    # Convert integer to binary and remove the '0b' prefix
    binary_str = bin(decimal_value)[2:]
    # Ensure the binary string length is a multiple of 4 by padding with leading zeros
    # The number of bits will be the length of the hex string * 4
    expected_length = len(hex_str) * 4
    binary_str = binary_str.zfill(expected_length)
    return binary_str

class InputTextBox(QPlainTextEdit):
    def __init__(self, parent, size = None, default_text = "", font_size = 16, is_accept_drop = False, is_read_only = False):
        super().__init__(parent)
        self.default_text = default_text
        self.is_accept_drop = is_accept_drop
        self.is_read_only = is_read_only
        # set size
        if size:
            self.setFixedSize(size[0], size[1])

        # set font size
        default_font = QFont()
        default_font.setPointSize(font_size)
        self.setFont(default_font)

        # default text
       # self.setPlaceholderText(self.default_text)

        # enable word wrapping
        self.setWordWrapMode(True)
        self.setLineWrapMode(True)

        # Enable drag and drop support
        self.setAcceptDrops(self.is_accept_drop)

        self.setReadOnly(self.is_read_only)

    ## don't change method name
    ## this is to override
    def focusInEvent(self, e):
        """clear the text box when the user focuses on the input text box"""
        if not self.toPlainText():
            self.clear()
            # change typed text colour
            self.setStyleSheet("color: red")
        super().focusInEvent(e)

    ## override
    def focusOutEvent(self, e):
        """Restore the default text if the text box is empty when focus is lost"""
        if not self.toPlainText():
            # change to default text
            #self.setPlaceholderText(self.default_text)
            self.setStyleSheet(f"color: red;")
        super().focusOutEvent(e)

    ## override
    def keyPressEvent(self, e):
        """ when the user is typing"""
        if not self.toPlainText():
            self.setStyleSheet("color: red;")
        super().keyPressEvent(e)
        
    ## override
    def dragEnterEvent(self,e):
        """ handle drag event to accept or ignore the drop"""
        # only allow drop if the text box is empty
        if not self.toPlainText():
            # didnt avoid -> (e.mimeData().hasText() or e.mineData().hasUrls())
            e.acceptProposedAction()
        else:
            # ignor the event if the box is not empty
            e.ignore()
        super().dragEnterEvent(e)

    ## override
    def dropEvent(self, e):
        """ handle drop event when the user drops an item"""
        if e.mimeData().hasText():
            # get the dropped text
            text = e.mimeData().text()
            # set the dropped text in the text box
            #self.setPlaceholderText(text)
        elif e.mimeData().hasUrls():
            # get the dropped URLs
            urls = e.mimeData().urls()
            # handle file URLs
            for url in urls:
                if url.isLocalFile():
                    file_path = url.toLocalFile()
                    # insert file path
                    #self.insertPlainText(f"File path: {file_path}")
                    self.update_text(file_path)
        # accept drop action
        e.accept()
        super().dropEvent(e)

    def reset(self):
        """ reset text box to default, clear text box, show default text"""
        self.clear()
        # default text
        #self.setPlaceholderText(self.default_text)
        self.setAcceptDrops(self.is_accept_drop)
        self.update_read_only(self.is_read_only)

    def get_binary_text(self):
        if is_binary(self.toPlainText()):
            return self.toPlainText()
        elif is_hexadecimal(self.toPlainText()):
            return hex_to_bin(self.toPlainText())
        return ''.join(format(ord(c), '08b') for c in self.toPlainText())

    def update_text(self, text):
        """ Replaces all text in the text box with the new text """
        self.clear()
        self.setPlainText(text)

    def is_file_path(self):
        text = self.toPlainText().strip()
        # Regex for file URL (file://) and file paths (Windows and Unix paths)
        file_path_pattern = r'^file:///([A-Za-z0-9_-]+(?:[\/][A-Za-z0-9_-]+)*\/?[A-Za-z0-9_\- .]+(?:\.[a-zA-Z0-9]+)?)$'
        if re.match(file_path_pattern, text):
            return True
        return False

    def update_read_only(self, is_read_only):
        self.setReadOnly(is_read_only)


