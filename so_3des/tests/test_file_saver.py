import unittest
from file_saver import FileSaver

class TestFileSaver(unittest.TestCase):
    def setUp(self):
        self.file_saver = FileSaver()

    def test_is_base64_image(self):
        png_header = b'\x89PNG\r\n\x1a\nSomeImageData'
        self.assertTrue(self.file_saver.is_base64_image(png_header))

        non_png_header = b'This is not a PNG file'
        self.assertFalse(self.file_saver.is_base64_image(non_png_header))

    def test_is_pdf(self):
        pdf_header = b'%PDF SomePDFData'
        self.assertTrue(self.file_saver.is_pdf(pdf_header))

        non_pdf_header = b'This is not a PDF file'
        self.assertFalse(self.file_saver.is_pdf(non_pdf_header))

    def test_is_video(self):
        video_header = b'\x00\x00\x00\x18ftypSomeVideoData'
        self.assertTrue(self.file_saver.is_video(video_header))

        non_video_header = b'This is not a video file'
        self.assertFalse(self.file_saver.is_video(non_video_header))

    def test_is_python_code(self):
        python_code = """# This is a Python script
        def my_function():
            pass
        """
        self.assertTrue(self.file_saver.is_python_code(python_code))

        non_python_code = "This is not Python code."
        self.assertFalse(self.file_saver.is_python_code(non_python_code))

    def test_is_plain_text(self):
        plain_text = "This is a plain text."
        self.assertTrue(self.file_saver.is_plain_text(plain_text))

        invalid_text = "\ud83d\udca9"  # Emoji that might fail certain encodings
        self.assertFalse(self.file_saver.is_plain_text(invalid_text))

    def test_get_filter(self):
        # for Base64-encoded PNG image
        png_header = '\x89PNG\r\n\x1a\nSomeImageData'
        self.assertEqual(
            self.file_saver.getFilter(png_header),
            ("Image Files (*.png)", bytes(png_header, 'latin1'))
        )

        # for PDF file
        pdf_header = '%PDF SomePDFData'
        self.assertEqual(
            self.file_saver.getFilter(pdf_header),
            ("PDF Files (*.pdf)", bytes(pdf_header, 'latin1'))
        )

        # for video file
        video_header = '\x00\x00\x00\x18ftypSomeVideoData'
        self.assertEqual(
            self.file_saver.getFilter(video_header),
            ("Movie Files (*.mov);;Movie Files (*.mp4)", bytes(video_header, 'latin1'))
        )

        # for Python file
        python_code = """# This is a Python script
        def my_function():
            pass
        """
        self.assertEqual(
            self.file_saver.getFilter(python_code),
            ("Python Files (*.py)", python_code)
        )

        # for plain text file
        plain_text = "This is a plain text file."
        self.assertEqual(
            self.file_saver.getFilter(plain_text),
            ("Text Files (*.txt)", plain_text)
        )

if __name__ == "__main__":
    unittest.main()