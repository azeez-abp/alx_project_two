"""Jwt decode and encode test"""

import unittest
from datetime import datetime, timezone

from app.libs.jwt import decode_, encodes_

# import time


class TestJWT(unittest.TestCase):

    def setUp(self):
        """Setup reusable attributes for the tests."""
        self.user_id = "12345"
        self.email = "user@example.com"

    def test_encodes_(self):
        """Test that encodes_ function returns a valid JWT token."""
        token = encodes_(self.user_id, self.email, 4567, "key")
        self.assertIsInstance(token, str)
        self.assertNotEqual(token, "")

    def test_decode_(self):
        """Test that decode_ function correctly decodes a JWT token."""
        token = encodes_(self.user_id, self.email, 4567, "key")
        decoded_data = decode_(token, "key")

        self.assertIsInstance(decoded_data,  tuple)
        self.assertEqual(decoded_data[0]["id"], self.user_id)
        self.assertEqual(decoded_data[0]["email"], self.email)

    def test_token_expiration(self):
        """Test that the token expires after the given timedelta."""
        token = encodes_(self.user_id, self.email, -456, "key")
        decoded_data = decode_(token, "key")
        self.assertIn("error", decoded_data[0].keys())


if __name__ == "__main__":
    unittest.main()
