""" Blueprint for API """

from flask import Blueprint  # type: ignore
from flask_restful import Api  # type: ignore
from v1.users.login import UserLogin  # type: ignore
from v1.users.register import UserRegister  # type: ignore
from v1.users.upload import Upload  # type: ignore

users_route = Blueprint("users_route", __name__, url_prefix="/api/v1/users/")
users_api = Api(users_route)
users_api.add_resource(UserLogin, "login")
users_api.add_resource(UserRegister, "register")
users_api.add_resource(Upload, "upload")
# from app.v1.users.login import *
# from app.v1.users.register import *
