import unittest

from app.libs.password import check_password, hash_password


class TestPasswordEncryption(unittest.TestCase):

    def test_hash_password(self):
        """Test that a plain text password is hashed correctly."""
        plain_text_password = "my_secret_password"
        hashed_password = hash_password(plain_text_password)

        # Ensure the hashed password is not None
        self.assertIsNotNone(hashed_password)
        # Ensure the hashed password is not the same as the plain text
        self.assertNotEqual(plain_text_password, hashed_password)
        # Ensure the hashed password is a string
        self.assertIsInstance(hashed_password, str)

    def test_check_password(self):
        """Test that the check_password function works correctly."""
        plain_text_password = "my_secret_password"
        wrong_password = "wrong_password"
        hashed_password = hash_password(plain_text_password)

        # Check correct password
        self.assertTrue(check_password(plain_text_password, hashed_password))
        # Check wrong password
        self.assertFalse(check_password(wrong_password, hashed_password))


if __name__ == "__main__":
    unittest.main()
