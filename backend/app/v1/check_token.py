from flask import request   # type: ignore
from flask_restful import Resource  # type: ignore
from libs.cookies import CookieHandler
from libs.jwt import decode_, encodes_
from libs.response_body import responseObject
from models.schemas.general.transaction import Session
from models.storage_engine import storage
from sqlalchemy import select  # type: ignore
from os import getenv


class CheckToken(Resource):
    def post(self):
        header = request.headers
        # print(decode_(header['Authorization']), "Header")

        if 'Authorization' not in header:
            return responseObject(False, True, "Bad header"), 400
        header = header["Authorization"]
        token_ = header.split(" ")[1]
        user_cookie = CookieHandler.get_cookie(request,
                                               getenv("SESSION_COOKIE_NAME"))
        
        if user_cookie is None:
            return responseObject(False, True,
                                  "Server did not recognise this client")
        user_id = user_cookie.split("__")[0]

        print(user_cookie, "cookie", user_id)

        def sess():
            access_token_payload = decode_(
                token_,
                getenv("SECRET_KEY")
                )
           
            access_token_has_expired = False
            if 'error' in list(access_token_payload[0].keys()):
                """Access token has expired"""
                access_token_has_expired = True

            """Check the cookie issued to the user
               if the cookie has expired:,logout
               else refresh token
            """

            if access_token_has_expired:
                """Get refresh token"""
                data = storage.get_instance().execute(select(Session).where(
                        Session.session_id == user_id,
                    )
                ).scalar()
                print(data.id, "DAR") 
                if data is not None:
                    print(data.session_token, "terterterter")
                    user_info = decode_(data.session_token,
                                        getenv("SECRET_KEY_REFRESH"))
                    
                    print(list(user_info[0].keys()), user_info) 
                    if 'error' in list(user_info[0].keys()):
                        return responseObject(False, True,
                                              'Session Expired'), 500
                    get_user_info = dict(user_info[0])
                    print(get_user_info, "USER_INFO")      
                    new_access_token = encodes_(get_user_info.get('id'),
                                                get_user_info.get('email'),
                                                1,
                                                getenv("SECRET_KEY"))
                    return responseObject(True, False,
                                          {"token": new_access_token,
                                           "token_status": "regenerated"}), 200
                else:
                    return responseObject(False, True,  "Session exired"), 404
            else:
                return responseObject(True, False,
                                      {"token": token_,
                                       "token_status": "valid"}), 200

        try:
            return sess()
        except Exception as e:
            print(e)
            return responseObject(False, True, f'{str(e)}'), 500
