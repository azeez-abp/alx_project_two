from datetime import datetime, timedelta, timezone

import jwt  # type: ignore

# from cryptography.hazmat.primitives import serialization  # type: ignore
"""
Logic
 generate access token
 generate refresh token
 send acces toke to user
 save fresh token to db
 save token expiration
 Access token expired
 decode fresh token to get user info
 refresh token expired, logout
"""


def encodes_(user_id: str, email: str, time_in_minute: int, secret: str) -> str:

    try:
        payload_data = {
            "id": user_id,
            "email": email,
            "exp": (
                datetime.now(timezone.utc) + timedelta(minutes=time_in_minute)
            ).timestamp(),
        }

        # paths = "~/.ssh/id_rsa"
        # with open(paths, "rb") as key_file:  # Use 'rb' to read as bytes
        #     private_key = key_file.read()

        # key = serialization.load_ssh_private_key(
        #     private_key,
        #     password=b"abp",  # Ensure this is the correct
        # password for your key
        # )
        token = jwt.encode(payload=payload_data, key=str(secret), algorithm="HS256")

        return token
    except Exception as e:
        return str(e)


def decode_(token: str, secret: str):
    # paths = "~/.ssh/id_rsa.pub"
    # with open(paths, "r") as key_:
    #  public_key = key_.read()
    # key = serialization.load_ssh_public_key(public_key.encode())

    try:
        data = jwt.decode(
            jwt=token,
            key=str(secret),
            algorithms=["HS256"],
        )

        return data, 200
    except Exception as e:
        return {"error": "token has expire", "message": str(e)}, 500
