from __future__ import absolute_import, print_function, unicode_literals

from pyramid.response import Response

from honeygen_pyramid.introspector import SQLAlchemyModel


class BaseView(object):
    """
    The base class of all the views.
    """

    def __init__(self, context, request):
        """
        The context here is passed by the resource.
        """
        self.request = request
        self.context = context


class ItemView(BaseView):
    """
    A view that represents an item in a collection (for example a user in a collection
    of users).
    Item views are called when requesting an element fro ma collection (example /users/1)
    """

    def read(self):
        """
        Read an item from a collection; Typically occurs with requests like GET /users/1
        :return: the item
        """
        entity = SQLAlchemyModel(self.context.entity)
        entity_class = self.context.model  # TODO: change
        serializer = entity_class.hg_get_serializer()()
        return serializer.serialize(entity)

    def update(self):
        """
        Update an item from a collection; Typically occurs with requests like PATCH /users/1
        :return: the updated item
        """
        return Response('You try to update an item', content_type='text/plain', status=200)

    def delete(self):
        """
        Delete an item from a collection; typically occurs with requests like DELETE /users/1
        """
        return Response('You try to delete an item', content_type='text/plain', status=200)


class CollectionView(BaseView):
    """
    A view that represents a collection, for example a collection of users.
    Usually bound to URLs like /users
    """

    def add(self):
        """
        Add an item to the collection
        :return: the new item
        """
        return Response('You try to add an element to a collection', content_type='text/plain', status=200)

    def list(self):
        """
        List items in the collection
        :return: a list of items
        """
        return Response('You try to list a collection', content_type='text/plain', status=200)

    def empty(self):
        """
        Empty the collection (delete all items)
        """
        return Response('You try to empty a collection', content_type='text/plain', status=200)
