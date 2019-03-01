import jsonschema
from django import forms
from django.utils.translation import gettext_lazy as _


def validate_json_schema(schema):
    try:
        jsonschema.validate({}, schema)
    except jsonschema.exceptions.SchemaError as error:
        msg = _('JSON Schema is not valid. Error: {error}')
        msg = msg.format(error=str(error))
        raise forms.ValidationError(msg)
    except jsonschema.exceptions.ValidationError:
        pass


def validate_json_instance(schema, instance):
    try:
        jsonschema.validate(schema, instance)
    except jsonschema.exceptions.ValidationError as error:
        msg = _('Instance does not comply with JSON schema. Error: {error}')
        msg = msg.format(error=str(error))
        raise forms.ValidationError(msg)


def validate_is_of_collection(collection, schema):
    is_of_collection = (
        collection
        .schemas
        .filter(name__exact=schema.name)
        .count() > 0)
    if not is_of_collection:
        msg = _('Schema {schema} is not part of collection {collection}')
        msg = msg.format(
            schema=schema.name,
            collection=collection.name)
        raise forms.ValidationError(msg)
