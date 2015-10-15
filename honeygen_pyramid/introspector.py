from inspect import isclass

from sqlalchemy import inspect
from sqlalchemy.orm import ColumnProperty, load_only


class Relationship(object):
    """
    Represent an entity's relationship.
    An entity has:
     - a name (string)
     - the type of the target model
     - the value (usually an ID or an array of IDs)
     - a flag that determines whether it is a *-to-one or *-to-many relationship
     - a flag that determines whether the value of the relationship has been filled. Important
     because None does not mean the value is not here, but that the value is None
    """

    def __init__(self, name, type, to_many=False, value=None, has_value=False):
        self.name = name
        self.to_many = to_many
        self.value = value
        self.type = type
        self.has_value = has_value


class Attribute(object):
    """
    Represent the attribute of an entity.
    An attribute has:
     - a name (string)
     - a value
     - a flag that determines whether the value of the attribute has been filled. Important
     because None does not mean the value is not here, but that the value is None
    """

    def __init__(self, name, value=None, has_value=False):
        self.name = name
        self.value = value
        self.has_value = has_value


class Model(object):
    """
    A model is a way to represent a model in an standardized and implementation-agnostic way.
    A model has :
     - a list of attributes
     - a list of relationships
    """

    def __init__(self, attributes, relationships, name, source, is_template=True):
        """
        Create a model from attributes and relationships
        :param attributes: a list of attributes
        :param relationships: a list of relationships
        :param name: the name of the model
        :param source: the entity from which the model was extracted
        :param is_template: a flag that indicates whether the model is a template or not.
        If the model is a template, the attributes and the relationship won't have values.
        """
        self.attributes = attributes
        self.relationships = relationships
        self.source = source
        self.name = name
        self.is_template = is_template


class SQLAlchemyModel(Model):
    """
    A SQLAlchemy model.
    Used to parse an SQLAlchemy object. Since this class is a subclass of a model, a SQLAlchemy
    model can be used in a standard way
    """

    def __init__(self, obj):
        """
        Create a model from a SQLAlchemy model class or model instance.
        If the passed object is a class, than the model will be a template for this class
        (attributes and relationships won't have value), but if the passed object is an instance
        of a SQLAlchemy class, then the Model will be complete (attributes and relationships will
        have values)
        :param obj: the instance or class of the SQLAlchemy model
        """
        if isclass(obj):
            super().__init__(attributes=self.get_attributes(obj),
                             relationships=self.get_relationships(obj),
                             name=obj.hg_name(),
                             source=None,
                             is_template=True)
        else:
            super().__init__(attributes=self.get_attributes(obj),
                             relationships=self.get_relationships(obj),
                             name=obj.hg_name(),
                             source=obj,
                             is_template=False)

    @staticmethod
    def get_attributes(obj):
        """
        Get all attributes of a SQLAlchemy model instance/class.

        The returned information about an attribute are:
         - its name (a string)
         - its value (only if the object is an instance)
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
            Get information about an attribute extracted from an SQLAlchemy column.
            The value will only be extracted if the object is an instance (not a class)
            """
            has_value = not isclass(obj)
            name = column.name
            value = getattr(obj, name) if has_value else None
            return Attribute(name, value, has_value=has_value)

        return [extract_from_sql_alchemy(column) for column in get_sqlalchemy_attributes(obj.__class__)]

    @staticmethod
    def get_relationships(obj):
        """
        Get all the relationships of a SQLAlchemy's model instance/class.
        The value of the relationship will only be extracted if the object is an instance (not a class)
        :param obj: an SQLAlchemy's model class/instance
        :return an array Relationship objects
        """

        def get_sqlalchemy_relationships(model_class):
            """
            Get all the relationships from an SQLAlchemy model's class
            :param model_class: the model's class
            :return: a list of SQLAlchemy relationships
            """
            return inspect(model_class).mapper.relationships.values()

        def extract_relationship(relationship, obj):
            """
            Extract information about an SQLAlchemy relationship
            :param relationship: the SQLAlchemy relationship
            :param obj: the SQLAlchemy model's class/instance to that owns the relationship
            :return a Relationship object
            """
            has_value = not isclass(obj)
            name = relationship.key
            to_many = relationship.uselist
            type = relationship.mapper.class_.hg_name()
            if not has_value:  # If the object is a class, we do not extract the value
                value = None
            else:
                value = getattr(obj, name)  # We extract the value of the relationship
                if value is not None:
                    # If the relationship points to a collection, value should be a query here (because by
                    # contract, the relationships should be tagged as lazy='dynamic'), and instead of fetching
                    # all the target entities, we can change the query to ask only for the IDs of the target
                    # entities (made in a single SQL request).
                    if to_many:
                        entities_only_ids = value.options(load_only('id')).all()
                        value = [entity_only_ids.id for entity_only_ids in entities_only_ids]
                    # If the value is another entity, we get its ID. No need to use "load_only('id')" here,
                    # since when fetching a single row in the database, it almost does not matter how many
                    # columns we read from the row.
                    # It could be annoying if we had eager loading on the target entity though.
                    else:
                        value = value.id
            return Relationship(name=name, value=value, type=type, to_many=to_many, has_value=has_value)

        # We get all the SQLAlchemy's relationships
        sqlalchemy_relationships = get_sqlalchemy_relationships(obj if isclass(obj) else obj.__class__)
        return [extract_relationship(rel, obj) for rel in sqlalchemy_relationships]
