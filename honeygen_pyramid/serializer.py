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
