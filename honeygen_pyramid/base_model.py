from __future__ import absolute_import, print_function, unicode_literals

from pyramid_sqlalchemy import metadata
from sqlalchemy.ext.declarative import declarative_base

from honeygen_pyramid.base_view import ItemView


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
        return 'hello'

    @classmethod
    def resource(cls):
        from honeygen_pyramid.base_resource import ResourceItem, ResourceCollection
        """
        Return the resource subtree for a model.
        The subtree is made of a ResourceCollection (for example '/users') and an ItemCollection
        (for example '/users/1) bound together.
        :return: the ResourceCollection
        """

        def resource_item(cls):
            subclass_name = cls.__name__ + 'ResourceItem'
            subclass_properties = {'model': cls}
            resource_item = type(subclass_name, (ResourceItem,), subclass_properties)
            return resource_item

        def resource_collection(cls, resource_item):
            subclass_name = cls.__name__ + 'ResourceCollection'
            subclass_properties = {'item_resource': resource_item}
            resource_collection = type(subclass_name, (ResourceCollection,), subclass_properties)
            return resource_collection

        return resource_collection(cls, resource_item(cls))

    @classmethod
    def get_view(cls):
        subclass_name = cls.__name__ + 'View'
        subclass_properties = {
            '__view_defaults__': {
                'context': cls.resource_item(),
                'renderer': 'json',
            }
        }
        item_view = type(subclass_name, (ItemView,), subclass_properties)
        return item_view


BaseModel = declarative_base(cls=BaseModel, metadata=metadata)
