from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.config import Configurator

from honeygen_pyramid.base_resource import Root
from honeygen_pyramid.jwt import get_user_jwt, JWTAuthenticationPolicy


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings,
                          root_factory='.base_resource.Root',
                          authentication_policy=JWTAuthenticationPolicy(),
                          authorization_policy=ACLAuthorizationPolicy())
    config.include('pyramid_sqlalchemy')
    config.add_request_method(get_user_jwt, name=str('user'), reify=True)
    config.scan()
    return config.make_wsgi_app()
