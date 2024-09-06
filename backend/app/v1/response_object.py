from typing import Dict, Type

from flask_restful import fields  # type: ignore

""" Define the expected structure for success and error responses"""


response_obj_template: Dict[str, Type[fields.Raw]] = {
    "data": fields.Raw,
    "success": fields.String,
    "user_id": fields.String,
    "email": fields.String,
    "error": fields.String(attribute="error"),
}
