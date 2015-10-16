import os

from pyramid import testing
import pytest
from webtest import TestApp

from honeygen_pyramid.tests.app.src import main
from honeygen_pyramid.tests.app.src.models import User


@pytest.fixture()
def pyramid_settings():
    return {
        'jwt.secret_key': 'MyAwesomeSecretKey',
    }


@pytest.yield_fixture(autouse=True)
def pyramid_config(pyramid_settings):
    """
    Set up a test pyramid registry and request for unit tests

    References:

    * http://docs.pylonsproject.org/projects/pyramid/en/latest/narr/testing.html#test-set-up-and-tear-down
    * http://docs.pylonsproject.org/projects/pyramid/en/latest/api/testing.html#pyramid.testing.setUp
    """
    yield testing.setUp(settings=pyramid_settings)
    testing.tearDown()


@pytest.fixture
def pyramid_app(pyramid_settings, monkeypatch, sql_session):
    """
    Set up a WebTest app for functional tests

    References:

    * http://docs.pylonsproject.org/projects/pyramid/en/latest/narr/testing.html#creating-integration-tests
    * http://webtest.readthedocs.org/en/latest/#quick-start
    """

    # Prevent SQL re-configuration with non-testing setup
    monkeypatch.setattr('pyramid_sqlalchemy.includeme', lambda c: None)

    app = main(global_config={}, **pyramid_settings)
    return TestApp(app, extra_environ={'repoze.tm.active': True})


@pytest.fixture(scope='session', autouse=True)
def pyramid_debug_authorization():
    os.environ['PYRAMID_DEBUG_AUTHORIZATION'] = '1'


@pytest.fixture
def user(sql_session):
    u = User(name='Brendan', age=18)
    sql_session.add(u)
    sql_session.flush()
    return u
