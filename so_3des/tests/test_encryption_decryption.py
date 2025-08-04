import unittest
import base64
from application import MainWindow
from PyQt5.QtWidgets import QApplication

class TestDecryption(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """ application instance."""
        cls.app = QApplication([])
        cls.window = MainWindow()

    def test_text_encryption_decryption(self):
        """ test encryption and decryption process for text"""

        # plaintext to test
        original_plaintext = "Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, pretium quis, sem. Nulla consequat massa quis enim. Donec pede justo, fringilla vel, aliquet nec, vulputate eget, arcu. In enim justo, rhoncus ut, imperdiet a, venenatis vitae, justo. Nullam dictum felis eu pede mollis pretium. Integer tincidunt. Cras dapibus. Vivamus elementum semper nisi. Aenean vulputate eleifend tellus. Aenean leo ligula, porttitor eu, consequat vitae, eleifend ac, enim. Aliquam lorem ante, dapibus in, viverra quis, feugiat a,"

        # Simulate the encryption process
        self.window.plaintext_input.update_text(original_plaintext)
        self.window.do_encryption()  # Call encryption method

        # Get encrypted text and keys after encryption
        encrypted_text = self.window.encrypted_text
        key1 = self.window.key1
        key2 = self.window.key2
        key3 = self.window.key3

        # Simulate the decryption process
        self.window.encrypted_input.update_text(encrypted_text)
        self.window.key1_input.update_text(key1)
        self.window.key2_input.update_text(key2)
        self.window.key3_input.update_text(key3)

        self.window.do_decryption()  # Call decryption method

        # Get the decrypted text
        decrypted_text = self.window.decrypted_output.toPlainText()

        # Remove all null characters from the decrypted text
        decrypted_text_clean = decrypted_text.replace('\x00', '')

        # Step 1: Save the cleaned decrypted result to a file
        with open("decrypted_output.txt", "w") as file:
            file.write(decrypted_text_clean)

        # Step 2: Read the saved file
        with open("decrypted_output.txt", "r") as file:
            saved_content = file.read()

        # Debugging: Check the original, decrypted, and saved content
        print(f"Original Text: '{original_plaintext}'")
        print(f"Decrypted Text (cleaned): '{decrypted_text_clean}'")
        print(f"Saved File Content: '{saved_content}'")

        # Step 3: Assert that the cleaned file content matches the original plaintext
        self.assertEqual(saved_content, original_plaintext,
                         f"File content does not match the original plaintext. Expected: '{original_plaintext}', but got: '{saved_content}'.")

    def test_file_encryption_decryption(self):
        """Test encryption and decryption process for files."""
        original_file_path = "/Users/veronicakwok/Desktop/Software_Optimization/2024-01-22_GroupProject_3DES/so_3des/requirement.txt"
        decrypted_file_path = "decrypted_file.txt"

        # Read the original file as binary data
        with open(original_file_path, "rb") as file:
            original_data = file.read()

        # Base64 encode the binary data to convert it into a string
        original_data_encoded = base64.b64encode(original_data).decode('utf-8')

        # Encrypt the Base64-encoded data
        self.window.plaintext_input.update_text(original_data_encoded)
        self.window.do_encryption()

        # Retrieve encrypted data and keys
        encrypted_text = self.window.encrypted_text
        key1 = self.window.key1
        key2 = self.window.key2
        key3 = self.window.key3

        # Decrypt the encrypted data
        self.window.encrypted_input.update_text(encrypted_text)
        self.window.key1_input.update_text(key1)
        self.window.key2_input.update_text(key2)
        self.window.key3_input.update_text(key3)
        self.window.do_decryption()

        # Retrieve the decrypted Base64-encoded data
        decrypted_data_encoded = self.window.decrypted_output.toPlainText()

        # Decode the Base64 string back into binary data
        decrypted_data = base64.b64decode(decrypted_data_encoded)

        # Save the decrypted data to a file
        with open(decrypted_file_path, "wb") as file:
            file.write(decrypted_data)

        # Compare the original and decrypted file contents
        self.assertEqual(decrypted_data, original_data,
                         "Decrypted file content does not match the original file.")

    @classmethod
    def tearDownClass(cls):
        """Clean up after tests."""
        del cls.window
        del cls.app


if __name__ == "__main__":
    unittest.main()
