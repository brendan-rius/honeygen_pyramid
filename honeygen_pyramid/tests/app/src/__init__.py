from __future__ import absolute_import, print_function, unicode_literals

from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.config import Configurator

from honeygen_pyramid import JWTAuthenticationPolicy, get_user_jwt


def main(global_config, **settings):
    config = Configurator(settings=settings,
                          root_factory='.base_resource.Root',
                          authentication_policy=JWTAuthenticationPolicy(),
                          authorization_policy=ACLAuthorizationPolicy())
    config.include('honeygen_pyramid')
    config.add_request_method(get_user_jwt, name=str('user'), reify=True)
    return config.make_wsgi_app()
