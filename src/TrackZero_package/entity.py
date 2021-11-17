from numbers import Number
from uuid import UUID
from datetime import datetime

class entity:
    def __init__(self, entity_type: str, entity_id: object) :
        """Creates a new entity

        Parameters:
        entity_type (str): The type of the entity.
        entity_id (str, Number, UUID): The id of the entity.

        """
        if not isinstance(entity_id, ( str, Number, UUID )):
            raise TypeError("Type %s is invalid for entity_id" % type(entity_id) )
        self.type = entity_type
        self.id = entity_id
        self.customAttributes = dict()

    def add_attribute(self, attribute_name: str, value):
        """Adds an attribute to the entity that holds a value

        Parameters:
        attribute_name (str): The name of the attribute on this entity.
        value (str, Number, UUID, datetime): The value of the new attribute.

        Returns:
        self for chaining.
        
        """
        if not isinstance(value, ( str, Number, UUID, datetime )):
            raise TypeError("Type %s is invalid for value" % type(value) )

        self.customAttributes.update({attribute_name: value})
        return self

    def add_entity_reference_attribute(self, attribute_name: str, referenced_attribute_type: str, referenced_attribute_id):
        """Adds an attribute to the entity that is linked to another entity

        Parameters:
        attribute_name (str): The name of the attribute on this entity.
        referenced_attribute_type (str): The type of the referenced entity.
        referenced_attribute_id (str, Number, UUID): The id of the referenced entity.

        Returns:
        self for chaining.

        """
        if not isinstance(referenced_attribute_id, ( str, Number, UUID )):
            raise TypeError("Type %s is invalid for entity_id" % type(referenced_attribute_id) )

        if attribute_name in self.customAttributes:
            self.customAttributes[attribute_name].append({ "type":referenced_attribute_type , "id":referenced_attribute_id})
        else:
            self.customAttributes[attribute_name] = [{ "type":referenced_attribute_type, "id":referenced_attribute_id}]

        return self