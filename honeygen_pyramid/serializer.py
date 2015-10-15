from abc import abstractmethod

import inflect

pluralizer = inflect.engine()


class Serializer(object):
    """
    Serializer for a SQLAlchemy object.
    This class can be extended to create different serializers.
    """

    @abstractmethod
    def serialize(self, model):
        """
        Take a full model and serializes it as a Python dictionary
        :param model: a Model
        :return: a dictionary representing the model
        """
        pass

    @abstractmethod
    def deserialize(self, obj, model_template):
        """
        Take a python dictionary serialized by this serializer and a model's template
        and fills the model with the values contained in the python dictionary
        :param obj: the dictionary
        :param model_template: a Model (without values) to fill
        :return: the same model, but filled with values from obj
        """
        pass

    @abstractmethod
    def serialize_list(self, models):
        pass

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
    def deserialize(self, obj, model_class):
        """
        This method receives a Python dictionary generated from a JSONAPI compliant json.
        Example:
        {
            'data': {
                'type': 'users',
                'id': '1',
                'attributes': {
                    'name': 'John Doe',
                    'age': '18'
                    'birth': '1996-11-15T00:16:00+00.00'
                }
            }
        }
        :param obj: the dictionary
        :param model_class: the template of the model to fill with the values contained in obj
        :return: the filled model
        """


    def serialize(self, model):
        return {
            'id': model.source.id,
            'type': pluralizer.plural(model.name),
            'data': self._serialize_data(model),
        }

    def serialize_list(self, models):
        return {
            'data': [self._serialize_in_list(model) for model in models]
        }

    def _serialize_in_list(self, model):
        return {
            'type': pluralizer.plural(model.name),
            'id': model.source.id,
            'attributes': self._serialize_attributes(model)
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
            data = [{'type': relationship.type, 'id': target} for target in relationship.value]
        else:
            data = {'type': relationship.type, 'id': relationship.value}
        return {'data': data}
