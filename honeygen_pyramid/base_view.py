from __future__ import absolute_import, print_function, unicode_literals
from pyramid.response import Response


class BaseView(object):
    def __init__(self, context, request):
        self.request = request
        self.context = context


class ItemView(BaseView):
    def read(self):
        return Response('You try to read an item', content_type='text/plain', status=200)

    def update(self):
        return Response('You try to update an item', content_type='text/plain', status=200)

    def delete(self):
        return Response('You try to delete an item', content_type='text/plain', status=200)


class CollectionView(BaseView):
    def add(self):
        return Response('You try to add an element to a collection', content_type='text/plain', status=200)

    def list(self):
        return Response('You try to list a collection', content_type='text/plain', status=200)

    def empty(self):
        return Response('You try to empty a collection', content_type='text/plain', status=200)
