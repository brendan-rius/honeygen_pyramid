from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.config import Configurator

from honeygen_pyramid.base_resource import Root
from honeygen_pyramid.exposed import all_models
from honeygen_pyramid.jwt import get_user_jwt, JWTAuthenticationPolicy
from .src import *  # It is important that we import all the models


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
    """
    We add all the views for the models to the Pyramid config.
    It is important for this method to run that all the models have been properly imported.
    :param config: the pyramid config to add the views to
    """
    for model_class, model_info in all_models.items():
        (item_context, item_view) = model_info['item_view']
        (collection_context, collection_view) = model_info['collection_view']
        config.add_view(item_view, context=item_context, request_method='GET', attr='read', renderer='json')
        config.add_view(item_view, context=item_context, request_method='PATCH', attr='update', renderer='json')
        config.add_view(item_view, context=item_context, request_method='DELETE', attr='delete', renderer='json')
        config.add_view(collection_view, context=collection_context, request_method='POST', attr='add', renderer='json')
        config.add_view(collection_view, context=collection_context, request_method='GET', attr='list', renderer='json')
        config.add_view(collection_view, context=collection_context, request_method='DELETE', attr='empty',
                        renderer='json')
