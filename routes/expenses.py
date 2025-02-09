
from fastapi import APIRouter, HTTPException
from models.expense import Expense,ExpenseUpdate
from core.expense import add_expense, get_pending_expenses, get_previous_month_payments, update_expense, \
    get_single_expenses

router = APIRouter(prefix="/expenses")

@router.post("/create", response_description="Add new expense")
async def create_expense(expense: Expense):
    expense_id = await add_expense(expense)
    return {"id": expense_id}

@router.get("/read/pending", response_description="List all pending expenses")
async def read_pending_expenses():
    expenses = await get_pending_expenses()
    return expenses

@router.get("/read/previous_month", response_description="Summary of previous month's payments")
async def read_previous_month_payments():
    expenses = await get_previous_month_payments()
    return expenses

@router.put("/update/{id}", response_description="Update an expense")
async def update_expense_data(id: str, expense: ExpenseUpdate):
    updated_expense = await update_expense(id, expense)
    if updated_expense:
        return updated_expense
    raise HTTPException(status_code=404, detail=f"Expense {id} not found")
@router.get("/read/single", response_description="List all single expenses")
async def read_single_expenses():
    expenses = await get_single_expenses()
    return expenses
