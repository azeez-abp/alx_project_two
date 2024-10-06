from os import getenv

from sqlalchemy import (  # type: ignore                                                                                                                                                                                                                                                                              # type: ignore
    delete,
    select,
)

from app.libs.cookies import CookieHandler  # type: ignore
from app.libs.response_body import responseObject  # type: ignore
from app.models.schemas.general.transaction import Session  # type: ignore
from app.models.storage_engine import storage  # type: ignore


def logout(request):
    # Get the user's session cookie

    user_cookie = CookieHandler.get_cookie(request, getenv("SESSION_COOKIE_NAME"))

    if user_cookie is None:
        return responseObject(False, True, "No active session found"), 400

    user_id = user_cookie.split("__")[0]
    try:
        session = (
            storage.get_instance()
            .execute(select(Session).where(Session.session_id == user_id))
            .scalar()
        )

        if session is None:
            return responseObject(False, True, "Session not found"), 404

        session = storage.get_instance()
        session.execute(delete(Session).where(Session.session_id == user_id))
        session.commit()
        # Clear the cookie
        CookieHandler.set_cookie(
            request, getenv("SESSION_COOKIE_NAME"), "", -7 * 24 * 60 * 60
        )

        return responseObject(True, False, "Successfully logged out"), 200

    except Exception as e:
        print(e)
        return responseObject(False, True, f"An error occurred: {str(e)}"), 500
