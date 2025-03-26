import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from crud import add_expense, get_expenses, delete_expense, update_expense
from dependencies import get_db
from pydantic import BaseModel
from datetime import date

# Модель для створення витрати
class ExpenseSchema(BaseModel):
    name: str
    amount_uah: int | float
    expense_date: date

class ExpenseResponseSchema(BaseModel):
    name: str
    amount_uah: int | float
    amount_usd: int | float
    expense_date: date


app = FastAPI()

# Запит для додавання витрат
@app.post("/expenses/")
async def create_expense(expense: ExpenseSchema, db: AsyncSession = Depends(get_db)):
    new_expense = await add_expense(db, expense.name, expense.amount_uah, expense.expense_date)
    return {"message": "Expense added successfully", "expense": new_expense}

# Запит для отримання витрат за період
@app.get("/expenses/")
async def read_expenses(start_date: date, end_date: date, db: AsyncSession = Depends(get_db)):
    expenses = await get_expenses(db, start_date, end_date)
    return {"expenses": expenses}

# Запит для видалення витрати
@app.delete("/expenses/{expense_id}")
async def remove_expense(expense_id: int, db: AsyncSession = Depends(get_db)):
    expense = await delete_expense(db, expense_id)
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    return {"message": "Expense deleted successfully"}

# Запит для оновлення витрати
@app.put("/expenses/{expense_id}")
async def modify_expense(expense_id: int, expense: ExpenseSchema, db: AsyncSession = Depends(get_db)):
    updated_expense = await update_expense(db, expense_id, expense.name, expense.amount_uah)
    if not updated_expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    return {"message": "Expense updated successfully", "expense": updated_expense}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
