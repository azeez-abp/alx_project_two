from flask_restful import Resource  # type: ignore
from app.models.schemas.general.transaction import Revenue  # type:ignore
from flask import request  # type:ignore
from app.libs.response_body import responseObject  # type:ignore
from sqlalchemy import select  # type:ignore
from app.models.storage_engine import storage  # type:ignore
from app.libs.auth import auth  # type:ignore

# parser = reqparse.RequestParser()
# parser.add_argument("date", type=str, required=True, help="Date is required")
# parser.add_argument("source", type=str, required=True, help="Source is required")
# parser.add_argument("amount", type=float, required=True, help="Amount is required")


class RevenueResource(Resource):
    def get(self, revenue_id=None):
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
                select(Revenue).limit(per_page).offset(offset_value)
            ).all()

            total_products = len(session.execute(select(Revenue)).fetchall())
            data = {
                  "data": [
                      { 
                        "id": revenue.id,
                        "description": revenue.description,
                        "user_id": revenue.user_id,
                        "source": revenue.source,
                        "amount": revenue.amount,
                        "created_at": revenue.created_at.isoformat(),
                    } for revenue in result],
                "page": page,
                "per_page": per_page,
                "total_products": total_products,
            }
            return responseObject(True, False, data)

        elif request.args.get("product_id"):
            
            revenue = (
                storage.get_instance().scalar(
                    select(Revenue).where(Revenue.id == request.args.get("product_id")))
               
            )

            if revenue:
                return (
                    responseObject(
                        True,
                        False,
                        {
                            "data": [
                                {
                                    "id": revenue.id,
                                    "description": revenue.description,
                                    "user_id": revenue.user_id,
                                    "source": revenue.source,
                                    "amount": revenue.amount,
                                }
                            ]
                        },
                    ),
                    200,
                )
            return responseObject(False, True, "No product match the id"), 404
        else:
            revenues = storage.get_instance().scalars(select(Revenue)).all()

            data = [
                {
                    "id": revenue.id,
                    "description": revenue.description,
                    "user_id": revenue.user_id,
                    "source": revenue.source,
                    "amount": revenue.amount,
                }
                for revenue in revenues
            ]
            return responseObject(True, False, {"data": data}), 200

    def post(self):
        args = request.get_json()
        try:
            new_revenue = Revenue(
                user_id=args.get("user_id"),
                description=args.get("description"),
                source=args.get("source"),
                amount=args.get("amount")
            )
            Revenue.add([new_revenue])
            return responseObject(True, False, "Revenue added successfully"), 201
        except Exception as e:
            return responseObject(False, True, f'{str(e)}'), 500
