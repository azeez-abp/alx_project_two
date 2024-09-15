"""Module for handling product resorces"""
from flask_restful import Resource  # type: ignore
from models.schemas.general.transaction import Product  # type: ignore
from flask import request  # type: ignore
from libs.response_body import responseObject  # type: ignore
from models.storage_engine import storage  # type: ignore
from sqlalchemy import select
from libs.method_not_in_resource import MethodNotInResource  # type: ignore
"""
parser = reqparse.RequestParser() from flask_restful
parser.add_argument("name", type=str, required=True,
help="Product name is required")
parser.add_argument("quantity", type=int, required=True,
help="Quantity is required")
parser.add_argument(
    "price_per_unit", type=float, required=True,
    help="Price per unit is required"
)
parser.add_argument("category", type=str, required=True,
help="Category is required")
parser.add_argument("description", type=str)
"""


class ProductResource(MethodNotInResource):
    """Class for handling product for
            for get  put put delete
                GET: handle there conditions
                based on request query, if page: get by pagination
                if product_id, get one item of the id
                else get all
                POST: handle adding the product
                PUT: handle updating the product
                DELETE: Handle removeal of product
            the method that will be called depend on the
            request method

    """
    def get(self, product_id=None):

        if request.args.get("page"):
            page = int(request.args.get('page', 1))
            per_page = int(request.args.get('per_page', 10))

            # Calculate the offset
            offset_value = (page - 1) * per_page

            # Get the database instance from storage
            query_engine = storage.get_instance()

            # Perform the query with pagination
            with query_engine.begin() as session:
                # Select products with limit and offset for pagination
                result = session.scalars(
                    select(Product).limit(per_page).offset(offset_value)
                ).all()

                total_products = session.scalar(select(Product).count())
                data = {
                    "products": [product.to_dict() for product in result],
                    "page": page,
                    "per_page": per_page,
                    "total_products": total_products
                }
                return responseObject(True, False, data)

        elif product_id:
            query_engine = storage.get_instance()
            product = storage.get_instance().scalar(
                select(Product).where(id == product_id)
                ).all()
            
            if product:
                return responseObject(True,False, {data: [{
                    "id": product.id,
                    "name": product.name,
                    "quantity": product.quantity,
                    "price_per_unit": product.price_per_unit,
                    "category": product.category,
                    "description": product.description,
                    "status":  product.status,
                    "created_at": product.created_at.isoformat(),
                }]}), 200
            return responseObject(False, True, "No prodcyt match the id"), 404
        else: 
            products = storage.get_instance().scalars(select(Product)).all()
    
            data = [
                {
                    "id": product.id,
                    "name": product.name,
                    "quantity": product.quantity,
                    "price_per_unit": product.price_per_unit,
                    "category": product.category,
                    "description": product.description,
                    "status":  product.status,
                    "created_at": product.created_at.isoformat(),
                }
                for product in products
            ]
            return responseObject(True, False, {"data": data}), 200

    def post(self):
        args = request.get_json()
        keys = args.keys()
        if "product_name" not in keys or not args["product_name"].strip():
            return responseObject(False, True, "Product name is required")
        try:
            
            new_product = Product(
                name=args["product_name"].strip(),
                quantity=args["quantity"],
                price_per_unit=args["price_per_unit"],
                category=args["category"],
                description=args.get("description", ""),
            )
            Product.add([new_product])
            # db.session.commit()
            return responseObject(True, False,
                                  "Product created successsfully"), 201
        except Exception as e:
            print(e)
            return responseObject(False, True, str(e)), 201
                  
    def put(self, product_id):
        args = request.get_json()
        product = Product.query.get(product_id)
        if product:
            product.name = args["name"]
            product.quantity = args["quantity"]
            product.price_per_unit = args["price_per_unit"]
            product.category = args["category"]
            product.description = args.get("description", product.description)

            return {"message": "Product updated successfully"}, 200
        return {"message": "Product not found"}, 404

    def delete(self, product_id):
        product = Product.query.get(product_id)
        if product:
            Product.delete(product)
            Product.save()
            return {"message": "Product deleted successfully"}, 200
        return {"message": "Product not found"}, 404
