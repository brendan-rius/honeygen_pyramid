from __future__ import absolute_import, print_function, unicode_literals
from honeygen_pyramid.models.user import UserModel


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


class UserResourceItem(ResourceItem):
    model = UserModel


class UserResourceCollection(object):
    entity_class = UserResourceItem

    def __getitem__(self, item):
        resource = self.entity_class(item)
        return resource


class Root(object):
    """
    The root used for traversal resource finding
    """

    """
    The children resources of this root. The name is reflected in the URL, thus the URL "/users" will call the child
    "users"
    """
    children = {
        'users': UserResourceCollection
    }

    def __init__(self, request):
        self.request = request

    def __getitem__(self, item):
        """
        Called when trying to get the resource for an URL.
        """
        resource = self.children[item]()
        return resource
