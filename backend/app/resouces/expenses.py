from flask_restful import Resource, reqparse  # type: ignore
from models.schemas.general.transaction import Expense  # type:ignore
from datetime import datetime

parser = reqparse.RequestParser()
parser.add_argument('date', type=str, required=True, help='Date is required')
parser.add_argument('description', type=str, required=True,
                    help='Description is required')
parser.add_argument('amount', type=float, required=True,
                    help='Amount is required')
parser.add_argument('category', type=str)


class ExpenseResource(Resource):
    def get(self, expense_id=None):
        if expense_id:
            expense = Expense.query.get(expense_id)
            if expense:
                return {
                    'id': expense.id,
                    'date': expense.date.strftime('%Y-%m-%d'),
                    'description': expense.description,
                    'amount': expense.amount,
                    'category': expense.category
                }, 200
            return {'message': 'Expense not found'}, 404
        expenses = Expense.query.all()
        return [{
            'id': expense.id,
            'date': expense.date.strftime('%Y-%m-%d'),
            'description': expense.description,
            'amount': expense.amount,
            'category': expense.category
        } for expense in expenses], 200

    def post(self):
        args = parser.parse_args()
        date = datetime.strptime(args['date'], '%Y-%m-%d')
        new_expense = Expense(
            date=date,
            description=args['description'],
            amount=args['amount'],
            category=args.get('category', '')
        )
        Expense.getInstance().add(new_expense)
        Expense.save()
        return {'message': 'Expense added successfully'}, 201
