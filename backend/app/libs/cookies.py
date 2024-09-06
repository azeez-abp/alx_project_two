from datetime import datetime, timedelta, timezone

from flask import Flask  # type: ignore

app = Flask(__name__)


class CookieHandler:
    @staticmethod
    def set_cookie(
        response, name, value, max_age, secure=False, httponly=False, samesite="None"
    ):
        # ("SameSite must be 'Strict', 'Lax', or 'None'."
        expires = datetime.now(timezone.utc) + timedelta(seconds=max_age)
        response.set_cookie(
            name,
            value + "__" + str(expires.timestamp()),
            expires=expires,
            secure=secure,
            httponly=httponly,
            samesite=samesite,  # put this in production
            path="/",
            domain="localhost",  # your domain name dont use ip
        )

    @staticmethod
    def get_cookie(request, name):
        return request.cookies.get(name)
