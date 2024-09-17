import random

from flask import request
from flask_restful import Resource  # type: ignore
from libs.password import hash_password  # type: ignore
from libs.response_body import responseObject  # type: ignore
from libs.send_email import EmailService  # type: ignore
from models.schemas.users.user import Users
from models.storage_engine import storage
from sqlalchemy import select, update  # type: ignore


class RequestPasswordRest(Resource):
    def post(self):
        req_data = request.get_json()
        if "email" not in req_data.keys():
            return responseObject(False, True, "Email is reuired"), 404
        otp = otp = random.randint(100000, 999999)

        try:
            has_session = storage.get_instance().scalar(
                select(Users).where(Users.email == req_data.get("email"))
            )

            if has_session is None:
                return (
                    responseObject(
                        False,
                        True,
                        f'User with email {req_data.get("email")} not found',
                    ),
                    404,
                )

            send_mail = EmailService("adioadeyoriazeez@gmail.com", "trrqdlvqadasyxqe")
            mail = send_mail.send_html_email(
                "OTP for Password reset", f"<h1>{otp} </h1>", req_data.get("email")
            )
            if mail is True:
                up = storage.get_instance()
                up.execute(
                    update(Users)
                    .where(Users.email == req_data.get("email"))
                    .values(otp=otp)
                )
                up.commit()
                return responseObject(True, False, "Email send sucessfull"), 200
            else:
                return responseObject(False, True, "Failed to send email"), 404
        except Exception as e:
            print(e)
            return responseObject(False, True, f"Error: {str(e)}"), 5000


class PasswordRest(Resource):
    def post(self):
        req_data = request.get_json()
        if "otp" not in req_data.keys():
            return responseObject(False, True, "Email is reuired"), 404
        if "password" not in req_data.keys():
            return responseObject(False, True, "Password is reuired"), 404

        try:
            has_session = storage.get_instance().scalar(
                select(Users).where(Users.otp == req_data.get("otp"))
            )

            if has_session is None:
                return (
                    responseObject(
                        False,
                        True,
                        f'User with opt email {req_data.get("otp")} not found',
                    ),
                    404,
                )

            up = storage.get_instance()
            up.execute(
                update(Users)
                .where(Users.otp == req_data.get("otp"))
                .values(password=hash_password(req_data.get("password")), otp="")
            )
            up.commit()
            return responseObject(True, False, "Email send sucessfull"), 200

        except Exception as e:
            return responseObject(False, True, f"Error: {str(e)}"), 5000
