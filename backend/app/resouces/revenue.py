from datetime import datetime

from flask_restful import Resource, reqparse  # type: ignore
from models.schemas.general.transaction import Revenue  # type:ignore

parser = reqparse.RequestParser()
parser.add_argument("date", type=str, required=True, help="Date is required")
parser.add_argument("source", type=str, required=True, help="Source is required")
parser.add_argument("amount", type=float, required=True, help="Amount is required")


class RevenueResource(Resource):
    def get(self, revenue_id=None):
        if revenue_id:
            revenue = Revenue.query.get(revenue_id)
            if revenue:
                return {
                    "id": revenue.id,
                    "date": revenue.date.strftime("%Y-%m-%d"),
                    "source": revenue.source,
                    "amount": revenue.amount,
                }, 200
            return {"message": "Revenue not found"}, 404
        revenues = Revenue.query.all()
        return [
            {
                "id": revenue.id,
                "date": revenue.date.strftime("%Y-%m-%d"),
                "source": revenue.source,
                "amount": revenue.amount,
            }
            for revenue in revenues
        ], 200

    def post(self):
        args = parser.parse_args()
        date = datetime.strptime(args["date"], "%Y-%m-%d")
        new_revenue = Revenue(date=date, source=args["source"], amount=args["amount"])
        Revenue.add(new_revenue)
        Revenue.save()
        return {"message": "Revenue added successfully"}, 201
