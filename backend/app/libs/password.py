"""Password encryption and decryption"""

import base64

import bcrypt


def hash_password(plain_text_password: str) -> str:
    """Encrypt a plain text password."""
    # Generate a salt
    salt = bcrypt.gensalt()
    # Hash the password with the salt
    hashed_password = bcrypt.hashpw(plain_text_password.encode("utf-8"), salt)
    # Encode the hashed password with base64
    return base64.b64encode(hashed_password).decode("utf-8")


def check_password(plain_text_password: str, hashed_password: str) -> bool:
    """Check if the provided plain text
    password matches the hashed password."""
    # Decode the base64 encoded hashed password
    decoded_hashed_password = base64.b64decode(hashed_password)
    # Check if the provided password matches the hashed password
    return bcrypt.checkpw(
        plain_text_password.encode("utf-8"),
        decoded_hashed_password
        )
