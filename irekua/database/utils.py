import jsonschema
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


FREE_SCHEMA = _('free')
GENERIC_SAMPLING_EVENT = _('generic sampling event')
GENERIC_SITE = _('generic site')
GENERIC_COLLECTION = _('generic collection')


def validate_json_schema(schema):
    try:
        jsonschema.validate({}, schema)
    except jsonschema.exceptions.SchemaError as error:
        msg = _('JSON Schema is not valid. Error: {error}')
        msg = msg.format(error=str(error))
        raise ValidationError(msg)
    except jsonschema.exceptions.ValidationError:
        pass


def validate_json_instance(schema, instance):
    try:
        jsonschema.validate(schema, instance)
    except jsonschema.exceptions.ValidationError as error:
        msg = _('Instance does not comply with JSON schema. Error: {error}')
        msg = msg.format(error=str(error))
        raise ValidationError(msg)


def validate_is_of_collection(collection, schema):
    if collection is None:
        return

    if schema.name == FREE_SCHEMA:
        return

    try:
        collection.schemas.get(name=schema.name)
    except collection.schemas.model.DoesNotExist:
        msg = _('Schema {schema} is not part of collection {collection}')
        msg = msg.format(
            schema=schema.name,
            collection=collection.name)
        raise ValidationError(msg)


def validate_are_same_term_type(source, target):
    if source.term_type != target.term_type:
        msg = _('Term types must be equal for synonyms ({type1} != {type2})')
        msg = msg.format(
            type1=source.term_type,
            type2=target.term_type)
        raise ValidationError(msg)


def validate_coordinates_and_geometry(geometry, latitude, longitude):
    if geometry.x != longitude or geometry.y != latitude:
        msg = _('Georeference and longitude-latitude do not coincide')
        raise ValidationError(msg)


def validate_event_type(event_type, item_type):
    try:
        item_type.event_types.get(name=event_type.name)
    except item_type.event_types.model.DoesNotExist:
        msg = _('Event type {event} is not valid for item type {item}')
        msg = msg.format(
            event=event_type.name,
            item=item_type.name)
        raise ValidationError(msg)


def empty_json():
    return {}
