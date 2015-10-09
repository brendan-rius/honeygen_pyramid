from sqlalchemy import inspect

from sqlalchemy.orm import ColumnProperty


class Relationship(object):
    """
    Represent an entity's relationship.
    An entity has:
     - a name (string)
     - a value
     - a flag that determines whether it is a *-to-one or *-to-many relationship
     - a flag that determines whether it is an optional relationship ot not
    """

    def __init__(self, name, value, to_many=False, optional=False):
        self.name = name
        self.to_many = to_many
        self.optional = optional
        self.value = value


class Attribute(object):
    """
    Represent the attribute of an entity.
    An attribute has a name (string), a value, and a type (string)
    """

    def __init__(self, name, value, type, optional=False):
        self.name = name
        self.value = value
        self.type = type
        self.optional = optional


class Model(object):
    """
    A model is a way to represent a model in an standardized and implementation-agnostic way.
    A model has :
     - a list of attributes
     - a list of relationships
    """

    def __init__(self, attributes, relationships, name, source):
        """
        Create a model from attributes and relationships
        :param attributes: a list of attributes
        :param relationships: a list of relationships
        :param name: the name of the model
        :param source: the entity from which the model was extracted
        """
        self.attributes = attributes
        self.relationships = relationships
        self.source = source
        self.name = name


class SQLAlchemyModel(Model):
    """
    A SQLAlchemy model.
    Used to parse an SQLAlchemy object. Since this class is a subclass of a model, a SQLAlchemy
    model can be used in a standard way
    """

    def __init__(self, sqlalchemy_entity):
        super().__init__(self.get_attributes(sqlalchemy_entity),
                         self.get_relationships(sqlalchemy_entity),
                         sqlalchemy_entity.hg_name(),
                         sqlalchemy_entity)

    @staticmethod
    def get_attributes(entity):
        """
        Get all attributes of a SQLAlchemy entity.

        The returned information about an attribute are:
         - its name (a string)
         - its value
         - its type (a string)

        In case of the attribute being extracted from an SQLAlchemy column, its type will be the result of
        column.type.

        :return an array of Attribute
        """

        def get_sqlalchemy_attributes(model):
            """
            Get all attributes from a SQLAlchemy model excluding:
             - primary keys
             - foreign keys
             - attributes that starts with an underscore
            """
            columns = []
            for attr in inspect(model).attrs:
                if isinstance(attr, ColumnProperty):
                    col = attr.columns[0]
                    if not col.primary_key and not col.foreign_keys and not col.name.startswith('_'):
                        columns.append(col)
            return columns

        def extract_from_sql_alchemy(column):
            """
            Get information about an attribute extracted from an SQLAlchemy column
            """
            if hasattr(column.type, 'impl'):
                typename = column.type.impl.__class__.__name__
            else:
                typename = column.type.python_type.__name__

            return Attribute(column.name, getattr(entity, column.name), typename, column.nullable)

        return [extract_from_sql_alchemy(column) for column in get_sqlalchemy_attributes(entity.__class__)]

    @staticmethod
    def get_relationships(entity):
        """
        Get all the visible relationships of a model.
        :return an array Relationship objects
        """

        def get_sqlalchemy_relationships(model):
            return inspect(model).mapper.relationships.values()

        def extract_relationship(relationship, entity):
            """
            Extract information about an SQLAlchemy relationship
            :param relationship: the SQLAlchemy relationship
            :return a Relationship object
            """
            is_relationship_optional = all(col.nullable for col in relationship.local_columns)
            name = relationship.key
            value = SQLAlchemyModel(getattr(entity, name))
            to_many = relationship.uselist
            return Relationship(name=name, value=value, to_many=to_many, optional=is_relationship_optional)

        relationships_attributes = get_sqlalchemy_relationships(entity.__class__)
        return [extract_relationship(rel, entity) for rel in relationships_attributes]
