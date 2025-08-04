import sys

from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from string_converter import StringConverter
from ui.buttons import Button
from ui.menu_bar import MenuBar
from ui.output_textbox import OutputTextBox
from ui.input_textbox import InputTextBox
from triple_des import TripleDES
from ui.status_bar import StatusBar
from ui.label import Label
from ui.popup_window import PopUpWindow
from file_saver import FileSaver

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.encrypted_text = ""
        self.key1 = ""
        self.key2 = ""
        self.key3 = ""
        self.triple_des = TripleDES()

        self.setWindowTitle("Triple Data Encryption Standard (3DES)")
        # horizontal position of top-left corner, vertical position of top-left corner, width, height
        self.setGeometry(100, 100, 1024, 768)

        # create a central widget for the main window
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # main layout
        self.main_layout = QVBoxLayout(self.central_widget)

        # manage pages
        self.stacked_widget = QStackedWidget()
        self.main_layout.addWidget(self.stacked_widget)

        #initialize item
        #Add Menu bar
        self.menu_bar = MenuBar(self, self, self.change_page)
        # status bar
        self.status_bar = StatusBar(self,"Ready for encryption")

        # Create pages
        self.create_pages()

        # Popup Window
        self.popup_window = PopUpWindow()

        # text converter
        self.converter = StringConverter()

        # file saver
        self.file_saver = FileSaver()

    def create_pages(self):
        """ create and load all pages"""
        # add pages to stacked
        self.stacked_widget.addWidget(self.show_introduction_page())
        self.stacked_widget.addWidget(self.show_credits_page())
        self.stacked_widget.addWidget(self.show_encryption_page())
        self.stacked_widget.addWidget(self.show_decryption_page())

        #set default_page
        self.init_ui()

    def change_page(self, page_index):
        self.stacked_widget.setCurrentIndex(page_index)
        self.update_decryption_page()

    def init_ui(self):
        """initial ui"""
        self.stacked_widget.setCurrentWidget(self.show_introduction_page())

    def show_introduction_page(self):
        """ clear existing content and load project info content"""
        self.status_bar.update_status_bar("Introduction")

        # create layout
        introduction_page = QWidget()
        introduction_page_layout = QVBoxLayout()
        introduction_page_layout.setAlignment(Qt.AlignTop)
        # margins, left, top, right, bottom
        introduction_page_layout.setContentsMargins(50, 10, 10, 10)

        introduction_text = """
        Welcome to the 3DES Encryption/Decryption App
        
        Enjoy encrypting and decrypting text and files using the 3DES algorithm
        
        Encryption and decryption can work for several file types like txt, png, pdf,.. etc
        
        You can always save the encryption keys and use them later for the decryption
        """
        introduction_label = Label(self, introduction_text, 16)

        # add widgets to layout
        introduction_page_layout.addWidget(introduction_label)

        # set the layout for the introduction page
        introduction_page.setLayout(introduction_page_layout)

        return introduction_page

    def show_credits_page(self):
        """ clear existing content and load credits content """
        self.status_bar.update_status_bar("Credits")

        credits_page = QWidget()
        credits_page_layout = QVBoxLayout()
        credits_page_layout.setAlignment(Qt.AlignTop)
        # margins, left, top, right, bottom
        credits_page_layout.setContentsMargins(50, 10, 10, 10)

        project_create_text = "Credits: \n\n Project create by: \n  - Bekir Bozokla \n  - Wonil Choi \n  - Meryem Hanyn \n  - Yujin Jeon \n  - Veronica Kwok \n  - Akin Çapar \n"
        study_info_text = "\nThis project was created at the University of Europe for Applied Sciences Potsdam. \n"
        professor_info_text = "Supervised by: Prof. Dr. Rand Kouatly \nSubject: Software Optimization (Winter Semester 2024/25) \n"
        credits_text = project_create_text + study_info_text + professor_info_text
        credits_label = Label(self, credits_text, 16)
        # add widgets to layout
        credits_page_layout.addWidget(credits_label)

        # set the layout
        credits_page.setLayout(credits_page_layout)

        return credits_page

    def show_encryption_page(self):
        """ clear existing content and load encryption content """
        self.status_bar.update_status_bar("Encryption")

        encryption_page = QWidget()
        encryption_page_layout = QVBoxLayout()

        # input
        plaintext_text = " Please type plaintext or drop a file below"
        plaintext_label = Label(self, plaintext_text, 12)
        self.plaintext_input = InputTextBox(self, [1000,300], is_accept_drop = True )
        encryption_page_layout.addWidget(plaintext_label)
        encryption_page_layout.addWidget(self.plaintext_input)

        # buttons
        encryption_page_button_layout = QHBoxLayout()
        encrypt_button = Button(self, [200, 50], "Encrypt", self.do_encryption)
        upload_plaintext_button = Button(self, [200, 50], "Upload File", lambda: self.upload_file(self.plaintext_input))
        rewrite_plaintext_button = Button(self, [200, 50], "Reset", self.do_encryption_page_reset)
        encryption_page_button_layout.addWidget(encrypt_button)
        encryption_page_button_layout.addWidget(upload_plaintext_button)
        encryption_page_button_layout.addWidget(rewrite_plaintext_button)
        encryption_page_layout.addLayout(encryption_page_button_layout)

        # output
        encryption_page_output_layout = QHBoxLayout()
        encryption_page_text_layout = QVBoxLayout()
        dncrypted_lable = Label(self, " Encrypted text: ", 12)
        self.encrypted_output = OutputTextBox(self,[690, 300])
        encryption_page_text_layout.addWidget(dncrypted_lable)
        encryption_page_text_layout.addWidget(self.encrypted_output)
        encryption_page_output_layout.addLayout(encryption_page_text_layout)

        encryption_page_keys_layout = QVBoxLayout()
        keys_label = Label(self," Keys: ", 12)
        self.key1_output = OutputTextBox(self, [300, (279 //3)])
        self.key2_output = OutputTextBox(self, [300, (279 //3)])
        self.key3_output = OutputTextBox(self, [300, (279 //3)])
        encryption_page_keys_layout.addWidget(keys_label)
        encryption_page_keys_layout.addWidget(self.key1_output)
        encryption_page_keys_layout.addWidget(self.key2_output)
        encryption_page_keys_layout.addWidget(self.key3_output)
        encryption_page_output_layout.addLayout(encryption_page_keys_layout)
        encryption_page_layout.addLayout(encryption_page_output_layout)

        # set the layout
        encryption_page.setLayout(encryption_page_layout)

        return encryption_page

    def show_decryption_page(self):
        """ clear existing content and load decryption content """
        self.status_bar.update_status_bar("Decryption")

        decryption_page = QWidget()
        decryption_page_layout = QVBoxLayout()

        # input
        decryption_page_input_layout = QHBoxLayout()
        decryption_page_text_layout = QVBoxLayout()
        default_text = " Please type encrypted text or drop a file below"
        encrypted_text_label = Label(self, default_text, 12)
        self.encrypted_input = InputTextBox(self, [690,300], default_text, is_accept_drop = True )
        decryption_page_text_layout.addWidget(encrypted_text_label)
        decryption_page_text_layout.addWidget(self.encrypted_input)
        decryption_page_input_layout.addLayout(decryption_page_text_layout)

        decryption_page_keys_layout = QVBoxLayout()
        keys_label = Label(self," Keys: ", 12)
        self.key1_input = InputTextBox(self, [300, (279 //3)])
        self.key2_input = InputTextBox(self, [300, (279 //3)])
        self.key3_input = InputTextBox(self, [300, (279 //3)])
        decryption_page_keys_layout.addWidget(keys_label)
        decryption_page_keys_layout.addWidget(self.key1_input)
        decryption_page_keys_layout.addWidget(self.key2_input)
        decryption_page_keys_layout.addWidget(self.key3_input)
        decryption_page_input_layout.addLayout(decryption_page_keys_layout)
        decryption_page_layout.addLayout(decryption_page_input_layout)

        # buttons
        decryption_page_buttons_layout = QHBoxLayout()
        decrypt_button = Button(self, [200, 50], "Decrypt", self.do_decryption)
        upload_encrypted_button = Button(self, [200, 50], "Upload File", lambda: self.upload_file(self.encrypted_input))
        rewrite_encrypted_button = Button(self, [200, 50], "Reset", self.do_decryption_page_reset)
        decryption_page_buttons_layout.addWidget(decrypt_button)
        decryption_page_buttons_layout.addWidget(upload_encrypted_button)
        decryption_page_buttons_layout.addWidget(rewrite_encrypted_button)
        decryption_page_layout.addLayout(decryption_page_buttons_layout)

        # output
        decrypted_text_label = Label(self, " Decrypted Text:", 12)
        self.decrypted_output = OutputTextBox(self, [1000, 300])
        # download_file_button = Button(self, [150, 50], "Download File", self.download_file)
        decryption_page_layout.addWidget(decrypted_text_label)
        decryption_page_layout.addWidget(self.decrypted_output)
        # decryption_page_layout.addWidget(download_file_button)
        decryption_page_layout.addLayout(decryption_page_input_layout)

        # set the layout
        decryption_page.setLayout(decryption_page_layout)

        return decryption_page

    def do_encryption(self):
        # do encryption
        self.plaintext_input.clearFocus()
        if self.plaintext_input.toPlainText() == "":
            self.encrypted_output.update_text("Please type plaintext or upload a file")
            self.popup_window.show_warning_popup("Warning", "Please type plaintext or upload a file.")
            self.status_bar.update_status_bar("Didn't found plaintext for encryption")
        elif self.plaintext_input.toPlainText():
            if self.plaintext_input.is_file_path():
                # convert file to string and do 3DES encryption method
                self.status_bar.update_status_bar("File converting to string")
                plaintext = self.plaintext_input.toPlainText()
                try:
                    binary_string = self.converter.file_to_string(plaintext)
                    output = self.triple_des.get_encrypted_text(binary_string)
                    self.status_bar.update_status_bar("File converted to string")
                except FileNotFoundError:
                    self.encrypted_output.update_text("File not found.")
                    self.status_bar.update_status_bar("File not found")
                    return
            else:
                # do 3DES encryption method
                self.status_bar.update_status_bar("Encrypting")
                binary_string = self.plaintext_input.get_binary_text()
                output = self.triple_des.get_encrypted_text(binary_string)
            # update output
            self.encrypted_text = self.converter.binary_to_hex(output)
            self.encrypted_output.update_text(self.encrypted_text)
            self.key1 = self.triple_des.get_key1_text()
            self.key1_output.update_text(self.key1)
            self.key2 = self.triple_des.get_key2_text()
            self.key2_output.update_text(self.key2)
            self.key3 = self.triple_des.get_key3_text()
            self.key3_output.update_text(self.key3)

            self.status_bar.update_status_bar("Encryption Done")

        print("Encryption Done, update text box")

    def do_decryption(self):
        self.status_bar.update_status_bar("Decrypting")
        # do decryption
        if self.encrypted_input.toPlainText() == "":
            self.decrypted_output.update_text("Please type encrypted text or upload a file")
            self.popup_window.show_warning_popup("Warning", "Please type encrypted text or upload a file.")
            self.status_bar.update_status_bar("Didn't found decrypted text for decryption")
        else:
            # add do 3DES decryption method
            self.triple_des.set_key1(self.key1_input.get_binary_text())
            self.triple_des.set_key2(self.key2_input.get_binary_text())
            self.triple_des.set_key3(self.key3_input.get_binary_text())
            output_binary = self.triple_des.get_decrypted_text(self.encrypted_input.get_binary_text())
            output_text = self.converter.binary_to_text(output_binary)
            self.decrypted_output.update_text(output_text)
            self.download_file(output_text)
            self.status_bar.update_status_bar("Decryption Done, update text box")
        print("Decryption Done, update text box")

    def upload_file(self, input_target):
        # select a file
        file_path, _ = QFileDialog.getOpenFileName( self, "Select File", "", "All Files (*);;Text Files (*.txt)" )
        # get a file path
        if file_path:
            input_target.update_text(f"file://{file_path}")
            self.status_bar.update_status_bar(f"Selected file: {file_path}")
        else:
            self.status_bar.update_status_bar("File selection cancelled.")

    def download_file(self, output_text=""):
        # download file
        options = QFileDialog.Options()
        filter,decoded = self.file_saver.getFilter(output_text)
        file_path, _ = QFileDialog.getSaveFileName(self,"Save File As", "",
                                                   filter,
                                                   options=options)
        if file_path:
            try:
                # checkfile extension and save the appropriate content
                if file_path.lower().endswith(".txt") or file_path.lower().endswith(".py"):
                    self.save_text(file_path,output_text)
                elif file_path.lower().endswith(".pdf"):
                    self.save_file(file_path,decoded)
                elif file_path.lower().endswith(".png"):
                    self.save_file(file_path,decoded)
                elif file_path.lower().endswith(".mov") or file_path.lower().endswith(".mp4"):
                    self.save_file(file_path,decoded)
                else:
                    self.status_bar.update_status_bar("This is unsupported file format.")
                self.status_bar.update_status_bar(f"File has been saved to {file_path}")
            except Exception as e:
                print (f"Error: {e}")
                self.status_bar.update_status_bar(f"Error: {e}")
        else:
            self.status_bar.update_status_bar("Please select file.")

    def save_text(self, file_path, output_text):
        with open(file_path, 'w') as file:
            cleaned_data = output_text.replace('\x00', '')  # Use a string for replacement
            file.write(cleaned_data)

    def save_file(self, file_path,output_text):
        if isinstance(output_text, str):
            output_text = bytes(output_text, 'latin1')  # Convert string to bytes
        with open(file_path, 'wb') as file:
            file.write(output_text)

    def do_encryption_page_reset(self):
        # input
        self.plaintext_input.reset()
        # output
        self.encrypted_output.reset()
        self.key1_output.reset()
        self.key2_output.reset()
        self.key3_output.reset()
        self.encrypted_text = ""
        self.key1 = ""
        self.key2 = ""
        self.key3 = ""

    def do_decryption_page_reset(self):
        # input
        self.encrypted_input.reset()
        self.key1_input.reset()
        self.key2_input.reset()
        self.key3_input.reset()
        self.encrypted_text = ""
        self.key1 = ""
        self.key2 = ""
        self.key3 = ""
        # able to type
        self.encrypted_input.update_read_only(False)
        self.key1_input.update_read_only(False)
        self.key2_input.update_read_only(False)
        self.key3_input.update_read_only(False)
        # output
        self.decrypted_output.reset()

    def update_decryption_page(self):
        if not self.encrypted_text == "":
            self.encrypted_input.update_read_only(True)
            self.encrypted_input.update_text(self.encrypted_text)
        else:
            self.encrypted_input.reset()
            self.encrypted_input.update_read_only(False)

        if not self.key1 == "":
            self.key1_input.update_read_only(True)
            self.key1_input.update_text(self.key1) #+ "update")
        else:
            self.key1_input.reset()

        if not self.key2 == "":
            self.key2_input.update_read_only(True)
            self.key2_input.update_text(self.key2) #+ "update")
        else:
            self.key2_input.reset()

        if not self.key3 == "":
            self.key3_input.update_read_only(True)
            self.key3_input.update_text(self.key3)# + "update")
        else:
            self.key3_input.reset()

