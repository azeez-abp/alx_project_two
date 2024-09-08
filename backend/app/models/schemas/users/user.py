#!/usr/bin/python
""" holds class Users"""
from models.schemas.base import BaseModel  # type: ignore
from models.storage_engine import storage  # type: ignore
from models.storage_engine.db import Base  # type: ignore
from sqlalchemy import Column, DateTime, String  # type: ignore
from sqlalchemy.orm import relationship  # type: ignore


class Users(BaseModel, Base):
    """Representation of a user"""

    __tablename__ = "users_account"
    user_id = Column(String(60), unique=True, nullable=False)
    first_name = Column(String(60), nullable=False)
    profile_pix = Column(String(120), nullable=False)
    middle_name = Column(String(60), nullable=False)
    last_name = Column(String(60), nullable=False)
    email = Column(String(225), nullable=False, unique=True)
    password = Column(String(225), nullable=False)  # Changed to LargeBinary
    gender = Column(String(15), nullable=False)
    date_of_birth = Column(DateTime, nullable=False)
    addresses = relationship(
        "Addresses", backref="users", cascade="all, delete, delete-orphan"
    )

    def __init__(self, **kward):
        """Initializes user"""
        super().__init__(**kward)


"""create table"""

Base.metadata.create_all(storage.get_engine())
