from models.schemas.base import BaseModel  # type: ignore
from models.storage_engine import storage  # type: ignore
from models.storage_engine.db import Base  # type: ignore
from sqlalchemy import Column, Date, Float, Integer, String, Text  # type: ignore

"""This table are created if the file that use them is added to root file app.py"""


class Product(BaseModel, Base):
    """Representation of product
    project/backend/app/models/schemas/general/transaction.py
    """

    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    quantity = Column(Integer, nullable=False)
    price_per_unit = Column(Float, nullable=False)
    category = Column(String(50), nullable=False)
    description = Column(Text)

    def __init__(self, **kward):
        """Initializes user"""
        super().__init__(**kward)


class Expense(BaseModel, Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False)
    description = Column(String(225), nullable=False)
    amount = Column(Float, nullable=False)
    category = Column(String(50))

    def __init__(self, **kward):
        """Initializes user"""
        super().__init__(**kward)


class Revenue(BaseModel, Base):
    __tablename__ = "revenue"

    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False)
    source = Column(String(120), nullable=False)
    description = Column(String(225), nullable=False)
    amount = Column(Float, nullable=False)

    def __init__(self, **kward):
        """Initializes parent"""
        super().__init__(**kward)


class Session(BaseModel, Base):
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    session_token = Column(Text(700), unique=True, nullable=False)
    session_id = Column(String(256), unique=True, nullable=False)
    expires_at = Column(Integer, nullable=False)

    def __init__(self, **kward):
        super().__init__(**kward)


Base.metadata.create_all(storage.get_engine())
