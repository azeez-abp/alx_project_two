""" Blueprint for API """

from flask import Blueprint  # type: ignore
from flask_restful import Api  # type: ignore
from app.v1.check_token import CheckToken  # type: ignore

token_route = Blueprint("check_token_route", __name__, url_prefix="/api/v1/")
# import the token_route  which is the blueprint
token_route_api = Api(token_route)
token_route_api.add_resource(CheckToken, "check_token")
