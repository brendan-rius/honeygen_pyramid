from __future__ import absolute_import, print_function, unicode_literals
from honeygen_pyramid.introspector import SQLAlchemyModel
from honeygen_pyramid.tests.app.src.models import User


def test_model_template():
    model = SQLAlchemyModel(User)
    assert model.is_template
    assert len(model.attributes) == 2
    assert len(model.relationships) == 2
    for attribute in model.attributes:
        assert not attribute.has_value
    for relationship in model.relationships:
        assert not relationship.has_value


def test_model(pyramid_app, user):
    model = SQLAlchemyModel(user)
    assert not model.is_template
    assert len(model.attributes) == 2
    assert len(model.relationships) == 2
    for attribute in model.attributes:
        assert attribute.has_value
    for relationship in model.relationships:
        assert relationship.has_value
