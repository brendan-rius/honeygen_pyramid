import inflect

from honeygen_pyramid.introspector import Attribute

pluralizer = inflect.engine()


class ComputedAttribute(Attribute):
    """
    An annotation used to add dynamic attributes to objects to serialize.
    For example, an object with two attributes "number_one" and "number_two"
    may want to have a computed attribute "sum" equal to "number_one" + "number_two".
    In this case, it can be done this way:

    ```
    @ComputedAttribute()
    def sum(self, entity):
        return entity.number_one + entity.number_two
    ```

    In case of conflict between the name of a "normal" attribute and the name of computed attribute,
    the computed attribute wins.

    You can specify the type of the computed attribute so it can be handled differently by serializers this way:
    ```
    @ComputedAttribute('Integer')
    def sum(self, entity):
        return entity.number_one + entity.number_two
    ```
    If the type is not specified, it will be "COMPUTED_ATTRIBUTE"

    By default, the name of the attribute will be the name of the function, but it can also be passed
    as a the third parameter like:

    ```
    @ComputedAttribute('Integer', 'awesome_sum')
    def sum(self, entity):
        return entity.number_one + entity.number_two
    ```

    The ComputedAttribute is also a subclass of Attribute and can be used where an attribute is used
    """

    def __init__(self, *args, **kwargs):
        argslen = len(args)
        if argslen == 0:  # @ComputedAttribute
            super().__init__(None, None, 'COMPUTED_ATTRIBUTE')
        elif argslen == 1:  # @ComputedAttribute('a_type')
            super().__init__(None, None, args[0])
        elif argslen == 2:  # @ComputedAttribute('a_type', 'a_name')
            super().__init__(args[1], None, args[0])

    def __call__(self, *args, **kwargs):
        """
        Called when the annotation is bound to a callable "func".
        We bind this object (the computed attribute) to the callable.
        It allows us to:
         1) tell that the callable is a computed attribute
         2) get the computed attribute of the callable, and thus get the attribute's name, value and type
        """
        func = args[0]
        func.__computed_attribute__ = self
        return func

    @staticmethod
    def is_present_on(func):
        """
        Check whether a callable is a computed attribute.
        :param func: the callable
        """
        return hasattr(func, '__computed_attribute__')


class Serializer(object):
    """
    Serializer for a SQLAlchemy object.
    This class can be extended to create different serializers.
    """

    """
    Some attributes to ignore during serialization
    """
    hidden = []

    def serialize(self, model):
        """
        Serialize a model
        :param model: the model
        :return: the serialized model
        """
        return None  # TODO implement

    def get_attributes(self, model):
        """
        Get all the attributes to serialize which are:
         - the attributes of the model that are not hidden
         - the computed attributes of the serializer

        :param hidden: an array of attributes' name representing the attributes to hide
        :return an array of Attribute
        """

        def extract_from_computed_attribute(name):
            """
            Get information about an attribute extracted from an "computed_attribute".
            """
            decorated_method = getattr(self, name)  # The method decorated by @ComputedAttribute
            computed_attribute = decorated_method.__computed_attribute__  # The computed attribute
            computed_attribute.name = computed_attribute.name or name  # We override the name eventually
            computed_attribute.value = decorated_method(model)  # We set the value of the computed attribute
            return computed_attribute  # We directly return the attribute, since ComputedAttribute is an Attribute

        def get_computed_attributes():
            """
            Get all the attributes name of the "computed attributes" of the serializer.
            An "computed attribute" is a function annotated with "computed_attribute"
            """

            def is_computed_attribute(attribute_name):
                """
                Check whether an attribute is annotated with "computed_attribute" or not
                """
                attribute = getattr(self, attribute_name)
                return ComputedAttribute.is_present_on(attribute)

            all_attributes_name = [name for name in dir(self)]
            return [attribute_name for attribute_name in all_attributes_name if is_computed_attribute(attribute_name)]

        computed_attributes = [extract_from_computed_attribute(name) for name in get_computed_attributes()]
        all_attributes = model.attributes + computed_attributes

        return [attribute for attribute in all_attributes if attribute.name not in self.hidden]

    def get_relationships(self, model):
        """
        Get all the relationships to serialize in a model
        :param model: the model
        :param hidden: the hidden attributes (if any)
        :return:
        """
        return [relationship for relationship in model.relationships if relationship.name not in self.hidden]

    def serialize_attribute(self, attribute):
        """
        Serialize an attribute
        :param attribute: the attribute
        :return: the serialized attribute
        """
        return attribute.value

    def serialize_relationship(self, relationship):
        """
        Serialize a relationship
        :param relationship: the relationship
        :return: the serialized relationship
        """
        return relationship.value


class JSONAPISerializer(Serializer):
    def serialize(self, model):
        return {
            'id': model.source.id,
            'type': pluralizer.plural(model.name),
            'data': self._serialize_data(model),
        }

    def serialize_as_rio(self, model):
        return {
            'id': model.id,
            'type': pluralizer.pluralize(model.name),
        }

    def _serialize_data(self, model):
        return {
            'attributes': self._serialize_attributes(model),
            'relationships': self._serialize_relationships(model),
        }

    def _serialize_attributes(self, model):
        return {attribute.name: self.serialize_attribute(attribute) for attribute in model.attributes}

    def _serialize_relationships(self, model):
        return {relationship.name: self.serialize_relationship(relationship) for relationship in model.relationships}

    def serialize_relationship(self, relationship):
        if relationship.to_many:
            data = [{
                        'type': relationship.type,
                        'id': target,
                    } for target in relationship.value]
        else:
            data = {
                'type': relationship.type,
                'id': relationship.value,
            }
        return {
            'data': data
        }
