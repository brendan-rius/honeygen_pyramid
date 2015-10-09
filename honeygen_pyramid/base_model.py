from __future__ import absolute_import, print_function, unicode_literals

from pyramid_sqlalchemy import metadata
from sqlalchemy.ext.declarative import declarative_base

from honeygen_pyramid.base_view import ItemView, CollectionView


class BaseModel(object):
    """
    The base model from which all model should inherit
    """

    @classmethod
    def hg_name(cls):
        """
        Get the name of the class.
        By default, it is just the lower version of the Python class name.
        Can be overridden to change name
        :return: the name
        """
        return cls.__name__.lower()

    @classmethod
    def hg_pluralized_name(cls):
        """
        Get the pluralized name of the class.
        This method use a basic pluralization strategy.
        Can be overridden
        :return: the pluralized name
        """
        name = cls.hg_name()
        if name.endswith('s'):
            return name + 'es'  # "address" -> "addresses"
        elif name.endswith('y'):
            return name[:-1] + 'ies'  # "availability" -> "availabilities"
        else:
            return name + 's'  # "word" -> "words"

    @classmethod
    def hg_get_by_id(cls, id):
        """
        This method get the entity represented by the class who has a certain identifier
        :param id: the identifier
        :return: the entity
        """
        return 'hello'

    @classmethod
    def hg_resource_subtree(cls):
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

        resource_item = resource_item(cls)
        resource_collection = resource_collection(cls, resource_item)
        cls.resource_item, cls.resource_collection = resource_item, resource_collection
        return resource_item, resource_collection

    @classmethod
    def hg_get_views(cls, resource_collection, resource_item):
        """
        Generate the view for the model (both the collection views and the item views)
        :param resource_collection: the resource collection for which to generate the collection view
        :param resource_item: the resource item for which to generate the item view
        :return: the item view, and the collection view
        """

        def item_view():
            subclass_name = cls.__name__ + 'View'
            subclass_properties = {}
            item_view = type(subclass_name, (ItemView,), subclass_properties)
            return resource_item, item_view

        def collection_view():
            subclass_name = cls.__name__ + 'CollectionView'
            subclass_properties = {}
            collection_view = type(subclass_name, (CollectionView,), subclass_properties)
            return resource_collection, collection_view

        return item_view(), collection_view()


BaseModel = declarative_base(cls=BaseModel, metadata=metadata)
