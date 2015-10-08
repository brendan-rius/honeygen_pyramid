from __future__ import absolute_import, print_function, unicode_literals


class BaseView(object):
    def __init__(self, context, request):
        self.request = request
        self.context = context


class ItemView(BaseView):
    def create(self):
        return 'Liste'

    def read(self):
        return 'Liste'

    def update(self):
        return 'Liste'

    def delete(self):
        return 'Liste'


class CollectionView(BaseView):
    def read(self):
        return 'Liste'

    def update(self):
        return 'Liste'
