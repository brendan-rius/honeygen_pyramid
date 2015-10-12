from __future__ import absolute_import, print_function, unicode_literals
from honeygen_pyramid.exposed import all_models


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
        self.entity = self.model.hg_get_by_id(id)


class ResourceCollection(object):
    """
    Represents a collection as a Pyramid resource. Bound to URLs like "/users" or
    "/users/5/friends"
    """

    """
    The class of the resource that represents an item of the collection.
    For example, if te collection is a collection of user, this will be the resource
    that represents an user.
    """
    item_resource = None
    """
    The class of the model represented by the resource
    """
    model = None

    def __init__(self):
        self.list = self.model.hg_get_all()

    def __getitem__(self, item):
        """
        Get the resource for an item in the collection.
        :param item: the identifier of the item in the collection
        :return a ResourceItem instantiated with the identifier
        """
        resource = self.item_resource(item)
        return resource


class Root(dict):
    """
    The root used for traversal resource finding
    """

    def __init__(self, request, **kwargs):
        super().__init__(**kwargs)
        self.request = request
        self.add_children()

    def add_children(self):
        """
        Add all the children to root.
        Read all the available models from the global all_models, get the resource subtree,
        and add them as children of this root resource
        """
        for model_class, model_info in all_models.items():
            name = model_info['url']  # If the model is "User", we want the URL to be "users"
            self[name] = model_info['resource_collection']()
