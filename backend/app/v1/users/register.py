import uuid

from flasgger.utils import swag_from  # type: ignore
from flask import request  # type: ignore
from flask_restful import Resource, marshal_with  # type: ignore
from libs.password import hash_password  # type: ignore
from models.schemas.general.address import Addresses  # type: ignore
from models.schemas.users.user import Users  # type: ignore
from models.storage_engine import storage  # type: ignore
from sqlalchemy import select  # type: ignore
from v1.response_object import response_obj_template  # type: ignore

""" Define the expected structure for success and error responses"""


class UserRegister(Resource):
    """Class for registering a user."""

    @marshal_with(response_obj_template)
    @swag_from("documentation/register.yml", methods=["POST"])
    def post(self):
        """Post methiod that handle user registration"""

        data_all = request.get_json()
        data = storage.get_instance().scalar(
            select(Users).where(Users.email == str(data_all["email"]))
        )
        if data is not None:
            error_response = {
                "success": None,
                "data": None,
                "error": f"User with {data_all['email']} already exist",
            }
            return error_response, 400

        user_id = uuid.uuid4()
        new_address = Addresses(
            user_id=user_id,
            street=data_all["street"],
            city=data_all["city"],
            state=data_all["state"],
            zip_code=data_all["zip_code"],
        )
        new_user = Users(
            user_id=user_id,
            first_name=data_all["first_name"],
            profile_pix=data_all["profile_image"],
            middle_name=data_all["middle_name"],
            last_name=data_all["last_name"],
            email=data_all["email"],
            password=hash_password(data_all["password"]),
            gender=data_all["gender"],
            date_of_birth=data_all["date_of_birth"],
            addresses=[new_address],
        )
        try:
            Users.add([new_user])
            response = {
                "success": "User successfully registered",
                "user_id": str(user_id),
                "email": data_all["email"],
                "error": None,
            }
            return response, 200
        except Exception as e:
            error_response = {
                "success": None,
                "data": None,
                "error": f"User registration failed {e._message}",
            }
            return error_response, 400
