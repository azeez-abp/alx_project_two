#!/usr/bin/python3
"""
Contains class BaseModel
"""
from datetime import datetime, timezone

from models.storage_engine import storage
from sqlalchemy import BigInteger, Column, DateTime, select  # type: ignore

time = "%Y-%m-%dT%H:%M:%S.%f"


class BaseModel:
    """The BaseModel class from which future classes will be derived"""

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=datetime.now(timezone.utc))

    def __init__(self, **kward):
        """Initialization of the base model"""
        print(kward, "ANOTHER")
        self.id
        self.created_at = datetime.now(timezone.utc)
        self.updated_at = self.created_at
        for key, value in kward.items():
            if key != "__class__":
                setattr(self, key, value)

    def __str__(self) -> str:
        """String representation of the BaseModel class"""
        return "[{:s}] ({:s}) {}".format(
            self.__class__.__name__, self.id, self.__dict__
        )

    @classmethod
    def add(cls: object, users: list) -> list:
        """method for adding objetc to table"""
        storage.get_instance().add_all(users)
        storage.get_instance().commit()
        return users

    @classmethod
    def query(cls_):
        storage.get_instance().scalar(select(cls_))

    # def delete(self):
    #     """delete the current instance from the storage"""
    #     storage.delete(self)
