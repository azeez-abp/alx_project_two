from os import getenv

from app.libs.cookies import CookieHandler  # type:ignore
from app.libs.jwt import decode_, encodes_  # type:ignore
from app.libs.response_body import responseObject  # type:ignore
from app.models.schemas.general.transaction import Session  # type:ignore
from app.models.storage_engine import storage  # type:ignore
from sqlalchemy import select  # type: ignore


def auth(request):
    header = request.headers

    if "Authorization" not in header:
        return responseObject(False, True, "Bad header"), 400
    header = header["Authorization"]
    token_ = header.split(" ")[1]
    user_cookie = CookieHandler.get_cookie(request, getenv("SESSION_COOKIE_NAME"))

    if user_cookie is None:
        return responseObject(False, True, "Server did not recognise this client")
    user_id = user_cookie.split("__")[0]

    def sess():
        access_token_payload = decode_(token_, getenv("SECRET_KEY"))

        access_token_has_expired = False
        if "error" in list(access_token_payload[0].keys()):
            """Access token has expired"""
            access_token_has_expired = True

        """Check the cookie issued to the user
            if the cookie has expired:,logout
            else refresh token
        """

        if access_token_has_expired:
            """Get refresh token"""
            data = (
                storage.get_instance()
                .execute(
                    select(Session).where(
                        Session.session_id == user_id,
                    )
                )
                .scalar()
            )

            if data is not None:
                print(data.session_token, "terterterter")
                user_info = decode_(data.session_token, getenv("SECRET_KEY_REFRESH"))

                if "error" in list(user_info[0].keys()):
                    return responseObject(False, True, "Session Expired"), 500
                get_user_info = dict(user_info[0])

                new_access_token = encodes_(
                    get_user_info.get("id"),
                    get_user_info.get("email"),
                    15,
                    getenv("SECRET_KEY"),
                )
                return (
                    responseObject(
                        True,
                        False,
                        {
                            "token": new_access_token,
                            "token_status": "regenerated",
                            "user_id": user_id,
                        },
                    ),
                    200,
                )
            else:
                return responseObject(False, True, "Session exired"), 404
        else:
            return (
                responseObject(
                    True,
                    False,
                    {"token": token_, "token_status": "valid", "user_id": user_id},
                ),
                200,
            )

    try:
        return sess()
    except Exception as e:
        print(e)
        return responseObject(False, True, f"{str(e)}"), 500
