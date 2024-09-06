import base64
import json
from datetime import datetime, timezone

from flask import jsonify, make_response, request
from flask_restful import Resource  # type: ignore
from libs.cookies import CookieHandler
from libs.jwt import decode_, encodes_


class CheckToken(Resource):
    def get(self):
        header = request.headers
        # print(decode_(header['Authorization']), "Header")
        token = decode_(header["Authorization"])
        print(token)

        if "error" in token.keys():
            """ "check if cookies is valid and regenerate token"""
            user_cookie = CookieHandler.get_cookie(request, "farm")

            if user_cookie is not None:
                time_ = float(user_cookie.split("__")[1])
                delta_time = time_ - datetime.now(timezone.utc).timestamp()
                if delta_time > 0:
                    """cookies is valid Re-fresh token"""
                    token_1 = header["Authorization"].split(".")[1]
                    print(token_1)

                    user = base64.b64decode(token_1).decode("utf-8")
                    user = json.loads(user)
                    print(user["id"])
                    return {"refrsh_token": encodes_(user["id"], user["email"])}
            return {"error": "login has expire"}

        return make_response(jsonify({"success": token}))
