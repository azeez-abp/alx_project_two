#!/usr/bin/env python3
"""This file is the login module for the user"""
from datetime import datetime, timedelta
from os import getenv

from flasgger.utils import swag_from  # type: ignore
from flask import jsonify, make_response, request  # type: ignore
from flask_restful import Resource  # type: ignore
from libs.cookies import CookieHandler  # type: ignore
from libs.jwt import encodes_  # type: ignore
from libs.password import check_password  # type: ignore
from libs.request_to_json import convert_request_to_json  # type: ignore
from libs.response_body import responseObject  # type: ignore
from models.schemas.general.transaction import Session
from models.schemas.users.user import Users  # type: ignore
from models.storage_engine import storage  # type: ignore
from sqlalchemy import select, update  # type: ignore


class UserLogin(Resource):
    # @marshal_with(response_obj_template)
    @swag_from("documentation/login.yml")
    def post(self):
        body = convert_request_to_json(request)
        try:
            data = storage.get_instance().scalar(
                select(Users).where(Users.email == str(body.get("email")))
            )

            if data is None:
                return (
                    responseObject(
                        False,
                        True,
                        f'User with email {body.get("email")}\
                                        not found',
                    ),
                    400,
                )

            pass_check = check_password(body.get("password"), data.password)

            if not pass_check:
                return responseObject(False, True, "Invalid credentail"), 400

            json_data = encodes_(data.user_id, data.email, 15, getenv("SECRET_KEY"))
            """7*24*60 7 days in minute"""
            json_data_refresh = encodes_(
                data.user_id, data.email, 7 * 24 * 60, getenv("SECRET_KEY_REFRESH")
            )
            print(json_data_refresh)

            response = make_response(
                jsonify(responseObject(True, False, {"data": json_data})), 200
            )
            response.headers["Content-Type"] = "application/json"
            CookieHandler.set_cookie(
                response,
                getenv("SESSION_COOKIE_NAME"),
                data.user_id,
                60 * 60 * 24 * 7,
                httponly=True,
                secure=False,
                samesite="Strict",
            )

            expires_at_timestamp = int((datetime.now() + timedelta(days=7)).timestamp())

            has_session = storage.get_instance().scalar(
                select(Session).where(Session.session_id == data.user_id)
            )

            if has_session is None:
                user_sesion = Session(
                    session_id=data.user_id,
                    expires_at=expires_at_timestamp,
                    session_token=json_data_refresh,
                )
                Session.add([user_sesion])
            else:
                """update the session"""
                print(data.user_id)
                s = storage.get_instance()
                up = s.execute(
                    update(Session)
                    .where(Session.session_id == data.user_id)
                    .values(session_token=json_data_refresh)
                )
                s.commit()
                print(up, "Up")
            return response
        except Exception as e:
            return responseObject(False, True, {"message": str(e)})
