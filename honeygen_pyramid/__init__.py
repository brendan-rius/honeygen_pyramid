from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.config import Configurator

from honeygen_pyramid.base_resource import Root
from honeygen_pyramid.exposed import all_models
from honeygen_pyramid.jwt import get_user_jwt, JWTAuthenticationPolicy
from .src import *


def main(global_config, **settings):
    config = Configurator(settings=settings,
                          root_factory='.base_resource.Root',
                          authentication_policy=JWTAuthenticationPolicy(),
                          authorization_policy=ACLAuthorizationPolicy())
    config.include('pyramid_sqlalchemy')
    config.add_request_method(get_user_jwt, name=str('user'), reify=True)
    _add_views(config)
    config.scan()
    return config.make_wsgi_app()


def _add_views(config):
    for model in all_models:
        (item_context, item_view), (collection_context, collection_view) = model.get_views()
        config.add_view(item_view, context=item_context, request_method='GET', attr='read')
        config.add_view(item_view, context=item_context, request_method='PATCH', attr='update')
        config.add_view(item_view, context=item_context, request_method='DELETE', attr='delete')
        config.add_view(collection_view, context=collection_context, request_method='POST', attr='add')
        config.add_view(collection_view, context=collection_context, request_method='GET', attr='list')
        config.add_view(collection_view, context=collection_context, request_method='DELETE', attr='empty')
