#!/usr/bin/python3
""""Module for setting cookie"""
from datetime import datetime, timedelta, timezone

from flask import Flask  # type: ignore
from app.libs.response_body import responseObject

app = Flask(__name__)


class CookieHandler:
    """Cookie setter"""

    @staticmethod
    def set_cookie(
        response, name, value, max_age, secure=False, httponly=False, samesite="None"
    ) -> dict:
        """
        set cooking
        Args:
            response (http Response): Resonse that wiil want to attck
                cookie to
            name (str): name of the cookie
            value (str): avlu eof the cookie
            max_age (str): time in string format that determines how long
                the coolie wi last
            secure (bool): this determine if the cookie is secure or not
                set to true in production and false in development
            httpOnly (bool): determine the accessible of the ookie in the
                browser.alway set to true
            samesite (str): this is policy that determins how the third party
                will access the site
        Return:
             dictionary {success:bool, error: bool, message}

        """
        # ("SameSite must be 'Strict', 'Lax', or 'None'."
        try:
            expires = datetime.now(timezone.utc) + timedelta(seconds=max_age)
          
            response.set_cookie(
                name,
                value + "__" + str(expires.timestamp()),
                expires=expires,
                secure=secure,
                httponly=httponly,
                samesite=samesite,  # put this in production
                path="/",
                # domain="localhost",
            )  # set for domain name
            # response.set_cookie(
            #     name,
            #     value + "__" + str(expires.timestamp()),
            #     expires=expires,
            #     secure=secure,
            #     httponly=httponly,
            #     samesite=samesite,  # put this in production
            #     path="/",
            #     domain="127.0.0.1",
            # )  # set for ip
            return responseObject({True, False, "Cookie set succfully"})
        except Exception as e:
            return responseObject(False, True, f"Failed to set cookie. Error: {str(e)}")

    @staticmethod
    def get_cookie(request, name):
        """
         set cooking
        Args:
            response (http Response): Resonse that wiil want to attck
                cookie to
            name (str): name of the cookie
         Return:
            dictionary {success:bool, error: bool, message}
        """
        return request.cookies.get(name)
