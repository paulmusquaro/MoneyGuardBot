from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from database import Expense
from currency import get_usd_exchange_rate
from datetime import date

async def add_expense(db: AsyncSession, name: str, amount_uah: float, expense_date: date):
    exchange_rate = await get_usd_exchange_rate()
    amount_usd = round(amount_uah / exchange_rate, 2)
    expense = Expense(name=name, amount_uah=amount_uah, amount_usd=amount_usd, date=expense_date)
    db.add(expense)
    await db.commit()
    await db.refresh(expense)
    return expense

async def get_expenses(db: AsyncSession, start_date: date, end_date: date):
    result = await db.execute(select(Expense).where(Expense.date.between(start_date, end_date)))
    return result.scalars().all()

async def delete_expense(db: AsyncSession, expense_id: int):
    expense = await db.get(Expense, expense_id)
    if expense:
        await db.delete(expense)
        await db.commit()
    return expense

async def update_expense(db: AsyncSession, expense_id: int, name: str, amount_uah: float):
    expense = await db.get(Expense, expense_id)
    if expense:
        exchange_rate = await get_usd_exchange_rate()
        expense.name = name
        expense.amount_uah = amount_uah
        expense.amount_usd = round(amount_uah / exchange_rate, 2)
        await db.commit()
        await db.refresh(expense)
    return expense