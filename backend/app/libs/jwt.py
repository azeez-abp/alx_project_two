from datetime import datetime, timedelta, timezone

import jwt  # type: ignore
from cryptography.hazmat.primitives import serialization  # type: ignore


def encodes_(user_id: str, email: str) -> str:

    try:
        payload_data = {
            "id": user_id,
            "email": email,
            "exp": (datetime.now(timezone.utc) + timedelta(minutes=1)).timestamp(),
        }
        paths = "~/.ssh/id_rsa"
        with open(paths, "rb") as key_file:  # Use 'rb' to read as bytes
            private_key = key_file.read()

        key = serialization.load_ssh_private_key(
            private_key,
            password=b"abp",  # Ensure this is the correct password for your key
        )

        token = jwt.encode(payload=payload_data, key=key, algorithm="RS256")

        return token
    except Exception as e:
        return str(e)


def decode_(token):
    paths = "~/.ssh/id_rsa.pub"
    try:
        with open(paths, "r") as key_:
            public_key = key_.read()
        key = serialization.load_ssh_public_key(public_key.encode())

        data = jwt.decode(
            jwt=token,
            key=key,
            algorithms=[
                "RS256",
            ],
        )
        return data
    except Exception as e:
        return {"error": "token has expire", "message": e.message}, 500
