import os
import glob
import json

from . import APP_DIRECTORY


NONE_SCHEMA_NAME = 'none.json'

SCHEMAS_SUBDIR = 'schemas'


def get_types_of_schema(subdir):
    schemas = []

    none_schema_path = os.path.join(
        APP_DIRECTORY, SCHEMAS_SUBDIR, NONE_SCHEMA_NAME)
    with open(none_schema_path, 'r') as jsonfile:
        schemas.append(json.load(jsonfile))

    schemas = glob.glob(os.path.join(
        APP_DIRECTORY, 'schemas', subdir, '*.json'))

    for schema in schemas:
        with open(schema, 'r') as jsonfile:
            schemas.append(json.load(jsonfile))

    titles = [schema['title'] for schema in schemas]

    return titles, schemas
