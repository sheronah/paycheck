
from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

class Expense(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    amount: float
    description: str
    due_date: date
    status: str  # "paid" or "pending"
    recurring: bool = False  # New field to indicate if the expense is recurring

class ExpenseA(BaseModel):
    id: Optional[str] = Field(None, alias="id")
    amount: float
    description: str
    due_date: date
    status: str  # "paid" or "pending"
    recurring: bool = False  # New field to indicate if the expense is recurring

class ExpenseUpdate(BaseModel):
    amount: Optional[float]
    description: Optional[str]
    due_date: Optional[date]
    status: Optional[str]
