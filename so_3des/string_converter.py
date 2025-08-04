import base64
import os
from PyQt5.QtWidgets import QFileDialog

class StringConverter:
    def file_to_string(self, file_path):
        """to read a file as binary data"""
        # check if a file URL (start with "file://"
        if file_path.startswith("file://"):
            # convert file URL to a local file path
            file_path = self.file_url_to_local_path(file_path)
        # open the file normally using the local path
        with open(file_path, 'rb') as file:
            binary_data = file.read()
        binary_string = ''.join(format(byte, '08b') for byte in binary_data)
        return binary_string


    def file_url_to_local_path(self, file_url):
        """ convert file URL to local file path"""
        # remove the "file://" part
        file_url = file_url[7:]

        # for window, replace "/ with "\\" if needed
        if os.name == "nt":
            file_url = file_url.replace("/", "\\")

        return file_url

    def write_text_to_file(self,file_path, text):
        if file_path:
            try:
                # Create and write to the file, create the file if it doesn't exist
                with open(file_path, 'w') as file:
                    file.write(text)  # Write text content to file
                print(f"Text has been written to {file_path}")
            except Exception as e:
                print(f"An error occurred: {e}")
        else:
            print("No file was selected.")

    def string_to_file(self, binary_data, output_file_path):
        """ to write binary data back to a file"""
        #binary_data = base64.b64decode(base64_data)
        with open(output_file_path, "wb") as file:
            file.write(binary_data)

    def binary_to_text(self,binary_str):
        n = 8
        binary_values = [binary_str[i:i + n] for i in range(0, len(binary_str), n)]
        text = ''.join(chr(int(bv, 2)) for bv in binary_values)
        return text

    def binary_to_hex(self, binary_str):
        #ensure the length of the binary string is a multiple of 4 (pad if necessary)
        padded_binary_str = binary_str.zfill(len(binary_str) + (4 - len(binary_str) % 4) % 4)

        # Group the binary string into 4-bit chunks and convert each chunk to a hexadecimal digit
        hex_str = ''.join(format(int(padded_binary_str[i:i+4], 2), 'X') for i in range(0, len(padded_binary_str), 4))
        return hex_str