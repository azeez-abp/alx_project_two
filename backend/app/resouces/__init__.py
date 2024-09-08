""" Blueprint for API """

from flask import Blueprint  # type: ignore
from flask_restful import Api  # type: ignore
from .expenses import ExpenseResource  # type: ignore
from .product import ProductResource  # type: ignore
from .revenue import RevenueResource  # type: ignore

resource_product_revenue_route = Blueprint("route_resource_product_revenue",
                                           __name__, url_prefix="/api/v1/")
# import the token_route  which is the blueprint
resource_product_revenue_route_api = Api(resource_product_revenue_route)

resource_product_revenue_route_api.add_resource(ExpenseResource, "expenses")
resource_product_revenue_route_api.add_resource(ProductResource, "product")
resource_product_revenue_route_api.add_resource(RevenueResource, "revenue")
