import base64
import unittest
from unittest.mock import mock_open, patch
import os

from six import binary_type

from string_converter import StringConverter

class TestStringConverter(unittest.TestCase):
    def setUp(self):
        """ set up test environment"""
        self.converter = StringConverter()

    @patch("builtins.open", new_callable=mock_open, read_data=b"Hello, world!")
    def test_file_to_string(self, mock_file):
        # test file_to_string with a local path
        result = self.converter.file_to_string("test_file.txt")
        expected_binary = ''.join(format(byte, '08b') for byte in b"Hello, world!")
        self.assertEqual(result, expected_binary)
        mock_file.assert_called_once_with("test_file.txt", "rb")

    @patch("builtins.open", new_callable=mock_open, read_data=b"%PDF-1.4\n%BinaryPDFData")
    def test_file_to_string_with_pdf(self, mock_file):
        # for PDF file
        result = self.converter.file_to_string("test_file.pdf")
        expected_binary = ''.join(format(byte, '08b') for byte in b"%PDF-1.4\n%BinaryPDFData")
        self.assertEqual(result, expected_binary)
        mock_file.assert_called_once_with("test_file.pdf", "rb")

    @patch("builtins.open", new_callable=mock_open, read_data=b"\x89PNG\r\n\x1a\nSomePNGData")
    def test_file_to_string_with_png(self, mock_file):
        # PNG file
        result = self.converter.file_to_string("test_image.png")
        expected_binary = ''.join(format(byte, '08b') for byte in b"\x89PNG\r\n\x1a\nSomePNGData")
        self.assertEqual(result, expected_binary)
        mock_file.assert_called_once_with("test_image.png", "rb")

    @patch("builtins.open", new_callable=mock_open, read_data=b"\x00\x00\x00\x18ftypqt  SomeMOVData")
    def test_file_to_string_with_mov(self, mock_file):
        # MOV file
        result = self.converter.file_to_string("test_video.mov")
        expected_binary = ''.join(format(byte, '08b') for byte in b"\x00\x00\x00\x18ftypqt  SomeMOVData")
        self.assertEqual(result, expected_binary)
        mock_file.assert_called_once_with("test_video.mov", "rb")

    def test_file_url_to_local_path_os(self):
        # test file_url_to_local_path on os
        with patch("os.name", "posix"):
            result = self.converter.file_url_to_local_path("file:///home/user/test_file.txt")
            # check if the URL is correctly converted to unix os path
            self.assertEqual(result, "/home/user/test_file.txt")

    def test_file_url_to_local_path_window(self):
        # test file_url_to_local_path on window
        with patch("os.name", "nt"):
            result = self.converter.file_url_to_local_path("file://C:/test_file.txt")
            # check if the URL is correctly converted to windows path
            self.assertEqual(result, "C:\\test_file.txt")

    @patch("builtins.open", new_callable=mock_open)
    @patch("builtins.print")
    def test_write_text_to_file(self, mock_print, mock_file):
        # test write_text_to_file
        self.converter.write_text_to_file("output.txt", "Hello world!")
        mock_file.assert_called_once_with("output.txt", "w")
        mock_file().write.assert_called_once_with("Hello world!")
        mock_print.assert_called_once_with("Text has been written to output.txt")

    @patch("builtins.open", new_callable=mock_open)
    def test_string_to_file(self, mock_file):
        # test string_to_file with binary data
        binary_data = b"binary content"
        self.converter.string_to_file(binary_data, "output.bin")
        mock_file.assert_called_once_with("output.bin", "wb")
        mock_file().write.assert_called_once_with(binary_data)

    def test_binary_to_text(self):
        # test binary_to_text
        # binary_str = binary "Hello"
        binary_str = "0100100001100101011011000110110001101111"
        result = self.converter.binary_to_text(binary_str)
        self.assertEqual(result, "Hello")

    def test_binary_to_hex(self):
        # test binary_to_hex
        # binary for "6D" (Hexadecimal)
        binary_str = "1101101"
        result = self.converter.binary_to_hex(binary_str)
        self.assertEqual(result, "6D")

    def test_binary_to_hex_padded(self):
        # test binary_to_hex with padding
        # binary for "5" (Hex), needs padding
        binary_str = "101"
        result = self.converter.binary_to_hex(binary_str)
        self.assertEqual(result, "5")

if __name__=="__main__":
    unittest.main()
