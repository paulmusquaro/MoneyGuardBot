import os
from sqlalchemy import Integer, String, Float, Date
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine


parent_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
database_path = os.path.join(parent_directory, "expenses.db")

DATABASE_URL = f"sqlite+aiosqlite:///{database_path}"
engine = create_async_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

class Base(DeclarativeBase):
    pass

class Expense(Base):
    __tablename__ = "expenses"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, index=True)
    amount_uah: Mapped[float] = mapped_column(Float)
    amount_usd: Mapped[float] = mapped_column(Float)
    date: Mapped[Date] = mapped_column(Date)