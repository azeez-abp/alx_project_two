from flask_restful import Resource  # type: ignore
from flask import request
from app.libs.auth import auth  # type: ignore


class CheckToken(Resource):
    def post(self):
        return auth(request)