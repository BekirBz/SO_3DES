
class FileSaver:
    def getFilter(self, output_text):
        decoded = bytes(output_text, 'latin1')
        # Check if the output_text contains valid Base64-encoded image data
        if self.is_base64_image(decoded):
            return "Image Files (*.png)",decoded

        # Check if it's likely a PDF file
        elif self.is_pdf(decoded):
            return "PDF Files (*.pdf)",decoded

        # Check if it's likely a MOV/MP4 file
        elif self.is_video(decoded):
            return "Movie Files (*.mov);;Movie Files (*.mp4)",decoded

        # Check if it's likely a Python file
        elif self.is_python_code(output_text):
            return "Python Files (*.py)",output_text

        # Check if it's just plain text
        elif self.is_plain_text(output_text):
            return "Text Files (*.txt)",output_text

        # Default to all files
        return "All Files (*)",None

    def is_base64_image(self,decoded):
        try:
            # Check if the text looks like a Base64-encoded PNG
            if decoded.startswith(b'\x89PNG\r\n\x1a\n'):  # PNG header
                return True
        except Exception:
            pass
        return False

    def is_pdf(self, decoded):
        try:
            # Check if the text looks like a PDF file (starts with '%PDF')
            if decoded.startswith(b'%PDF'):
                return True
        except Exception:
            pass
        return False

    def is_video(self, decoded):
        try:
            # Check if the text looks like a MOV/MP4 file (starts with 'ftyp' magic number)
            if decoded[:4] == b'\x00\x00\x00\x18' and decoded[4:8] == b'ftyp':
                return True
        except Exception:
            pass
        return False

    def is_python_code(self, text):
        # Check if the text looks like Python code (simple check for common patterns)
        return text.strip().startswith('#') or 'def ' in text

    def is_plain_text(self, text):
        # Check if the text is plain text by trying to decode it as UTF-8
        try:
            text.encode('utf-8')
            return True
        except UnicodeEncodeError:
            return False
