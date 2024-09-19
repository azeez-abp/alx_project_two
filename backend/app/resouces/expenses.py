from flask import request
from flask_restful import Resource, reqparse  # type: ignore
from models.schemas.general.transaction import Expense  # type:ignore
from libs.auth import auth
from libs.response_body import responseObject
from models.storage_engine import storage  # type: ignore
from sqlalchemy import select, delete, update

# parser = reqparse.RequestParser()
# parser.add_argument("date", type=str, required=True, help="Date is required")
# parser.add_argument(
#     "description", type=str, required=True, help="Description is required"
# )
# parser.add_argument("amount", type=float, required=True, help="Amount is required")
# parser.add_argument("category", type=str)


class ExpenseResource(Resource):
    def get(self, expense_id=None):
        if not auth(request)[0].get("success"):
            return responseObject(False, True, "Unauthorized access"), 401

        if request.args.get("page"):
            page = int(request.args.get("page", 1))
            per_page = int(request.args.get("per_page", 10))

            # Calculate the offset
            offset_value = (page - 1) * per_page

            # Get the database instance from storage
            session = storage.get_instance()

            # Select products with limit and offset for pagination
            result = session.scalars(
                select(Expense).limit(per_page).offset(offset_value)
            ).all()

            total_products = len(session.execute(select(Expense)).fetchall())
            data = {
                "data": [
                    {
                        "id": product.id,
                        "amount": product.amount,
                        "category": product.category,
                        "description": product.description,
                        "created_at": product.created_at.isoformat(),
                    }
                    for product in result
                ],
                "page": page,
                "per_page": per_page,
                "total_products": total_products,
            }
            return responseObject(True, False, data)

        elif request.args.get("product_id"):

            product = storage.get_instance().scalar(
                select(Expense).where(Expense.id == request.args.get("product_id"))
            )

            if product:
                return (
                    responseObject(
                        True,
                        False,
                        {
                            "data": [
                                {
                                    "id": product.id,
                                    "amount": product.amount,
                                    "category": product.category,
                                    "description": product.description,
                                    "created_at": product.created_at.isoformat(),
                                }
                            ]
                        },
                    ),
                    200,
                )
            return responseObject(False, True, "No product match the id"), 404
        else:
            products = storage.get_instance().scalars(select(Expense)).all()

            data = [
                {
                    "id": product.id,
                    "amount": product.amount,
                    "category": product.category,
                    "description": product.description,
                    "created_at": product.created_at.isoformat(),
                }
                for product in products
            ]
            return responseObject(True, False, {"data": data}), 200

    def post(self):
        if not auth(request)[0].get("success"):
            return responseObject(False, True, "Unauthorized access"), 401
        args = request.get_json()
        try:
            new_expense = Expense(
                user_id=args["user_id"],
                description=args["description"],
                amount=args["amount"],
                category=args.get("category", ""),
            )
            Expense.add([new_expense])
            return responseObject(True, False, "Expense add successfully"), 201
        except Exception as e:
            return responseObject(False, True, f"{str(e)}"), 500
