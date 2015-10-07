from sqlalchemy import (
    Column,
    Integer,
    Text,
)

from honeygen_pyramid.base_model import BaseModel

__all__ = ['NoSuchUserException', 'UserModel']


class NoSuchUserException(Exception):
    pass


class UserModel(BaseModel):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    age = Column(Integer)
