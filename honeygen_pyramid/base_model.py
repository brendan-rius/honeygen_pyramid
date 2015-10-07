from __future__ import absolute_import, print_function, unicode_literals
from pyramid_sqlalchemy import metadata, Session
from sqlalchemy.ext.declarative import declarative_base


class BaseModel(object):
    """
    The base model from which all model should inherit
    """

    @classmethod
    def get_by_id(cls, id):
        """
        This method get the entity represented by the class who has a certain identifier
        :param id: the identifier
        :return: the entity
        """
        return Session.query(cls).get(id)


BaseModel = declarative_base(cls=BaseModel, metadata=metadata)
