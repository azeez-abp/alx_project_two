#!/usr/bin/python
""" holds class Users"""
from app.models.schemas.base import BaseModel  # type: ignore
from app.models.storage_engine import storage  # type: ignore
from app.models.storage_engine.db import Base  # type: ignore
from sqlalchemy import Column, DateTime, String  # type: ignore
from sqlalchemy.orm import relationship  # type: ignore

from app.models.schemas.general.address import Addresses  # Assuming Addresses is defined here
from app.models.schemas.general.transaction import Product  # Ensure Product is imported after Users
from app.models.schemas.general.transaction import Expense
from app.models.schemas.general.transaction import Revenue


class Users(BaseModel, Base):
    """Representation of a user"""

    __tablename__ = "users_account"
    user_id = Column(String(60), unique=True, nullable=False)
    first_name = Column(String(60), nullable=False)
    profile_pix = Column(String(120), nullable=False)
    middle_name = Column(String(60), nullable=False)
    last_name = Column(String(60), nullable=False)
    email = Column(String(225), nullable=False, unique=True)
    password = Column(String(225), nullable=False)
    gender = Column(String(15), nullable=False)
    date_of_birth = Column(DateTime, nullable=False)  # type: ignore
    otp = Column(String(20))
    addresses = relationship(
        "Addresses", backref="users", cascade="all, delete, delete-orphan"
    )
    products = relationship(
        "Product", backref="users", cascade="all, delete, delete-orphan"
    )
    expenses = relationship(
        "Expense",
        backref="users",
        cascade="all, delete, delete-orphan"
    )
    revenue = relationship(
        "Revenue",
        backref="users",
        cascade="all, delete, delete-orphan"
    )

    def __init__(self, **kward):
        """Initializes user"""
        super().__init__(**kward)


"""create table"""

Base.metadata.create_all(storage.get_engine())
