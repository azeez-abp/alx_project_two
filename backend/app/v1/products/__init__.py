""" Blueprint for API """

from flask import Blueprint  # type: ignore
from flask_restful import Api  # type: ignore
from resouces.product import ProductResource   # type: ignore


products_route = Blueprint("products_route", __name__, url_prefix="/api/v1/product/")
products_route_api = Api(products_route)
products_route_api.add_resource(ProductResource, 'add')
