from flask import request  # type: ignore
from flask_restful import Resource  # type: ignore
from app.libs.logout import logout  # type: ignore


class LogoutResource(Resource):
    def post(self):
        return logout(request)