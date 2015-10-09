from __future__ import absolute_import, print_function, unicode_literals

from sqlalchemy import (
    Column,
    Integer,
    Text,
    ForeignKey,
)

from sqlalchemy.orm import relationship

from honeygen_pyramid.base_model import BaseModel
from honeygen_pyramid.exposed import exposed


@exposed
class User(BaseModel):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(Text)
    age = Column(Integer)

    best_friend_id = Column(Integer, ForeignKey('users.id'))
    best_friend = relationship('User')
