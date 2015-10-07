from __future__ import absolute_import, print_function, unicode_literals

from pyramid.view import view_config, view_defaults

from honeygen_pyramid.resources.user import UserResourceItem, UserResourceCollection

__all__ = ['UserView', 'UsersView']


@view_defaults(context=UserResourceItem, renderer='json')
class UserView(object):
    def __init__(self, context, request):
        self.request = request
        self.context = context

    @view_config(permission='read')
    def get(self):
        return self.context


@view_defaults(context=UserResourceCollection)
class UsersView(object):
    def __init__(self, context, request):
        self.request = request
        self.context = context

    @view_config()
    def get(self):
        return 'Liste'
