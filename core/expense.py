
from models.expense import Expense, ExpenseUpdate,ExpenseA
from middleware.database import expense_collection
from bson import ObjectId
from datetime import datetime, timedelta

async def add_expense(expense: Expense):
    expense = expense.dict()
    result = await expense_collection.insert_one(expense)
    return str(result.inserted_id)

async def get_pending_expenses():
    expenses = await expense_collection.find({"status": "pending"}).to_list(1000)
    final_in = []
    for r in expenses:
        r = dict(r)
        final_in.append(ExpenseA(
            id=ObjectId(r['_id']).__str__(),
            amount=r['amount'],
            description=r['description'],
            due_date=r['due_date'],
            status=r['status'],
            recurring =r['recurring'],

        ))
    return final_in

async def get_previous_month_payments():
    today = datetime.today()
    first_day_of_current_month = datetime(today.year, today.month, 1)
    last_day_of_previous_month = first_day_of_current_month - timedelta(days=1)
    first_day_of_previous_month = datetime(last_day_of_previous_month.year, last_day_of_previous_month.month, 1)

    rs = await expense_collection.find({
        "due_date": {"$gte": first_day_of_previous_month, "$lt": first_day_of_current_month},
        "status": "paid"
    }).to_list(1000)


    return ExpenseA(
        id=ObjectId(rs[0]['_id']).__str__(),
        amount=rs[0]['amount'],
        description=rs[0]['description'],
        due_date=rs[0]['due_date'],
        status=rs[0]['status'],
        recurring=rs[0]['recurring'],
    )

async def update_expense(id: str, expense: ExpenseUpdate):
    await expense_collection.update_one({"_id": ObjectId(id)}, {"$set": expense.dict(exclude_unset=True)})
    rs = await expense_collection.find_one({"_id": ObjectId(id)})
    return ExpenseA(
        id=ObjectId(rs['_id']).__str__(),
        amount=rs['amount'],
        description=rs['description'],
        due_date=rs['due_date'],
        status=rs['status'],
        recurring=rs['recurring'],
    )

async def get_single_expenses():
    rs= await expense_collection.find({"recurring": False}).to_list(1000)
    return ExpenseA(
        id=ObjectId(rs['_id']).__str__(),
        amount=rs['amount'],
        description=rs['description'],
        due_date=rs['due_date'],
        status=rs['status'],
        recurring=rs['recurring'],
    )
