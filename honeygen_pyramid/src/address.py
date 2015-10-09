from __future__ import absolute_import, print_function, unicode_literals
from sqlalchemy import Column, Integer, Text, ForeignKey

from sqlalchemy.orm import backref, relationship

from honeygen_pyramid.base_model import BaseModel
from honeygen_pyramid.exposed import exposed


@exposed
class Address(BaseModel):
    __tablename__ = 'addresses'
    id = Column(Integer, primary_key=True)
    city = Column(Text, nullable=False)

    owner_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    owner = relationship('User', backref=backref('addresses'))
