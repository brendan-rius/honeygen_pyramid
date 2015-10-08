from __future__ import absolute_import, print_function, unicode_literals
from honeygen_pyramid.exposed import all_models

__all__ = ['ResourceItem', 'ResourceCollection', 'Root']


class ResourceItem(object):
    """
    Represent an item from a collection as Pyramid resource.
    For example the URL '/users/5' is the item 5 of the collection
    "users".
    It is also a resource, because we can have URLs such as "/users/5/friends"
    """

    """
    The class of the model represented by the resource
    """
    model = None

    def __init__(self, id):
        """
        Create the resource, and binds the corresponding entity
        to it. For example, if we access the URL '/users/5', or '/users/5/friends',
        this resource will contain the fifth user.

        :param id: the identifier of the user in the collection
        """
        self.entity = self.model.get_by_id(id)


class ResourceCollection(object):
    item_resource = None

    def __getitem__(self, item):
        resource = self.item_resource(item)
        return resource


class Root(dict):
    """
    The root used for traversal resource finding
    """

    def __init__(self, request, **kwargs):
        super().__init__(**kwargs)
        self.request = request
        for model in all_models:
            name = model.__name__.lower() + 's'
            collection = model.resource()
            self.add_children(name, collection())

    def add_children(self, name, resource):
        self[name] = resource
