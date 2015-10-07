from pyramid.config import Configurator

from honeygen_pyramid.base_resource import Root
from .views import *
from .models import *


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings, root_factory=Root)
    config.include('pyramid_sqlalchemy')
    config.scan()
    return config.make_wsgi_app()
