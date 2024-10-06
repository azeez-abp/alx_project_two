"""This file contain code for image upload
   from next js frontend to pillow
"""

from flasgger.utils import swag_from  # type: ignore
from flask import request  # type: ignore
from flask_restful import Resource, marshal_with  # type: ignore
from app.libs.upload_file import upload_image
from app.v1.response_object import response_obj_template


class Upload(Resource):
    @marshal_with(response_obj_template)
    @swag_from("documentation/upload.yml")
    def post(self):
        """Endpoit for image upload,"""
        file = request.files
        return upload_image(file["profile_image"])
