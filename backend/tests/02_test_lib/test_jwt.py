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
        token = encodes_(self.user_id, self.email)
        self.assertIsInstance(token, str)
        self.assertNotEqual(token, "")

    def test_decode_(self):
        """Test that decode_ function correctly decodes a JWT token."""
        token = encodes_(self.user_id, self.email)
        decoded_data = decode_(token)
        self.assertIsInstance(decoded_data, dict)
        self.assertEqual(decoded_data["id"], self.user_id)
        self.assertEqual(decoded_data["email"], self.email)

    def test_token_expiration(self):
        """Test that the token expires after the given timedelta."""
        token = encodes_(self.user_id, self.email)
        decoded_data = decode_(token)
        expiration_time = datetime.fromtimestamp(decoded_data["exp"], tz=timezone.utc)
        current_time = datetime.now(timezone.utc)
        self.assertLess(current_time, expiration_time)

    # def test_decode_with_expired_token(self):
    #     """Test that decoding an expired token raises an exception."""
    #     token = encodes_(self.user_id, self.email)
    #     time.sleep(61)
    #     with self.assertRaises(Exception):
    #         decode_(token)


if __name__ == "__main__":
    unittest.main()
