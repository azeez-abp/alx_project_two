from flask_restful import Resource, reqparse  # type: ignore
from models import Product  # type: ignore


parser = reqparse.RequestParser()
parser.add_argument('name', type=str, required=True,
                    help='Product name is required')
parser.add_argument('quantity', type=int,
                    required=True, help='Quantity is required')
parser.add_argument('price_per_unit',
                    type=float,
                    required=True, help='Price per unit is required')
parser.add_argument('category', type=str,
                    required=True, help='Category is required')
parser.add_argument('description', type=str)


class ProductResource(Resource):
    def get(self, product_id=None):
        if product_id:
            product = Product.query.get(product_id)
            if product:
                return {
                    'id': product.id,
                    'name': product.name,
                    'quantity': product.quantity,
                    'price_per_unit': product.price_per_unit,
                    'category': product.category,
                    'description': product.description
                }, 200
            return {'message': 'Product not found'}, 404
        products = Product.query.all()
        return [{
            'id': product.id,
            'name': product.name,
            'quantity': product.quantity,
            'price_per_unit': product.price_per_unit,
            'category': product.category,
            'description': product.description
        } for product in products], 200

    def post(self):
        args = parser.parse_args()
        new_product = Product(
            name=args['name'],
            quantity=args['quantity'],
            price_per_unit=args['price_per_unit'],
            category=args['category'],
            description=args.get('description', '')
        )
        Product.add(new_product)
        # db.session.commit()
        return {'message': 'Product added successfully'}, 201

    def put(self, product_id):
        args = parser.parse_args()
        product = Product.query.get(product_id)
        if product:
            product.name = args['name']
            product.quantity = args['quantity']
            product.price_per_unit = args['price_per_unit']
            product.category = args['category']
            product.description = args.get('description', product.description)
    
            return {'message': 'Product updated successfully'}, 200
        return {'message': 'Product not found'}, 404

    def delete(self, product_id):
        product = Product.query.get(product_id)
        if product:
            db.session.delete(product)
            db.session.commit()
            return {'message': 'Product deleted successfully'}, 200
        return {'message': 'Product not found'}, 404
