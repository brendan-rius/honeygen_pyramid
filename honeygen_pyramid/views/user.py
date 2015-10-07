from __future__ import absolute_import, print_function, unicode_literals

from pyramid.response import Response
from pyramid.view import view_config, view_defaults

from honeygen_pyramid.resources.user import UserResourceItem, UserResourceCollection

__all__ = ['UserView', 'UsersView']


@view_defaults(context=UserResourceItem)
class UserView(object):
    def __init__(self, context, request):
        self.request = request

    @view_config()
    def my_view(self):
        return Response("<h1>Hello {}</h1>".format(self.request.remote_addr), content_type='text/html', status_int=200)


@view_defaults(context=UserResourceCollection)
class UsersView(object):
    def __init__(self, context, request):
        self.request = request

    @view_config()
    def my_view(self):
        return Response("<h1>Hello {}</h1>".format(self.request.remote_addr), content_type='text/html', status_int=200)
