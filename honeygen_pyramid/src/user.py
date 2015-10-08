from __future__ import absolute_import, print_function, unicode_literals

from sqlalchemy import (
    Column,
    Integer,
    Text,
)

from honeygen_pyramid.base_model import BaseModel


class User(BaseModel):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    age = Column(Integer)
