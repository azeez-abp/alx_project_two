import io
import unittest
from unittest.mock import MagicMock, patch

from werkzeug.datastructures import FileStorage  # type: ignore

from app.libs.upload_file import upload, upload_image


class TestImageUpload(unittest.TestCase):
    """File uplaod test for booth blob and form-data"""

    def test_upload_valid_extension(self):
        """Test uploading with a valid file extension."""
        # this file data is  not good
        file_data = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAUA"

        file_name = "test.png"
        response = upload(file_data, file_name)
        self.assertNotIn("file_name", response)
        self.assertNotIn("output_path", response)

    def test_upload_invalid_extension(self):
        """Test uploading with an invalid file extension."""
        file_data = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAUA"
        file_name = "test.txt"
        response = upload(file_data, file_name)
        self.assertIn("error", response)

    def test_upload_image_invalid_file_path(self):
        """Test upload_image with an invalid file path."""
        response, status_code = upload_image(None)
        self.assertEqual(status_code, 400)
        self.assertIn("error", response)

    @patch("app.libs.upload_file.Image")
    def test_upload_image_valid(self, mock_image):
        """Test upload_image with a valid image."""
        file_storage = FileStorage(
            stream=MagicMock(spec=io.BytesIO), filename="test.jpg"
        )
        response, status_code = upload_image(file_storage, resize=True)
        self.assertEqual(status_code, 200)
        self.assertIn("data", response)

    @patch("app.libs.upload_file.Image")
    def test_upload_image_exception(self, mock_image):
        """Test upload_image handling an exception."""
        mock_image.open.side_effect = Exception("Mocked exception")
        file_storage = FileStorage(
            stream=MagicMock(spec=io.BytesIO), filename="test.jpg"
        )
        response, status_code = upload_image(file_storage)
        self.assertEqual(status_code, 400)
        self.assertIn("error", response)


if __name__ == "__main__":
    unittest.main()
