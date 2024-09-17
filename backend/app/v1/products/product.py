#!/user/bin/bash
# from flask_restful import Resource  # type: ignore
# from flask import request  # type: ignore
# from models.schemas.general.transaction import Product  # type: ignore
# from models.storage_engine import storage as db  # type: ignore
# from libs.response_body import responseObject  # type: ignore

# # parser = reqparse.RequestParser()
# # parser.add_argument('name', type=str, required=True, help='Item Name is required')
# # parser.add_argument('quantity', type=int, required=True, help='Quantity is required')
# # parser.add_argument('price_per_unit', type=float, required=True, help='Price per unit is required')
# # parser.add_argument('category', type=str, required=True, help='Category is required')
# # parser.add_argument('description', type=str)


# class ProductResource(Resource):
#     def get(self, product_id=None):

#         try:
#             if product_id:
#                 product = Product.query.get(product_id)
#                 if product:
#                     return {
#                         "id": product.id,
#                         "name": product.name,
#                         "quantity": product.quantity,
#                         "price_per_unit": product.price_per_unit,
#                         "category": product.category,
#                         "description": product.description,
#                     }, 200
#                 return {"message": "Product not found"}, 404
#             products = Product.query.all()
#             return [
#                 {
#                     "id": product.id,
#                     "name": product.name,
#                     "quantity": product.quantity,
#                     "price_per_unit": product.price_per_unit,
#                     "category": product.category,
#                     "description": product.description,
#                 }
#                 for product in products
#             ], 200
#         except Exception as e:
#             return responseObject(False, True, str(e))

#     def post(self):
#         args = request.get_jsoN()
#         print("POST CALL")
#         try:
#             new_product = Product(
#                 name=args["name"],
#                 quantity=args["quantity"],
#                 price_per_unit=args["price_per_unit"],
#                 category=args["category"],
#                 description=args.get("description", ""),
#             )
#             db.session.add(new_product)
#             db.session.commit()
#             return {"message": "Product added successfully"}, 201
#         except Exception as e:
#             return responseObject(False, True, str(e))

#     def put(self, product_id):
#         args = request.args()
#         product = Product.query.get(product_id)
#         if product:
#             product.name = args["name"]
#             product.quantity = args["quantity"]
#             product.price_per_unit = args["price_per_unit"]
#             product.category = args["category"]
#             product.description = args.get("description", product.description)
#             db.session.commit()
#             return {"message": "Product updated successfully"}, 200
#         return {"message": "Product not found"}, 404

#     def delete(self, product_id):
#         product = Product.query.get(product_id)
#         if product:
#             db.session.delete(product)
#             db.session.commit()
#             return {"message": "Product deleted successfully"}, 200
#         return {"message": "Product not found"}, 404
