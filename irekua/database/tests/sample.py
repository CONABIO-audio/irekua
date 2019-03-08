from collections import namedtuple

Schema = namedtuple('Schemas', ['name', 'schema'])


ANNOTATION_TOOL = 'Sample Annotation Tool'
ANNOTATION_TYPE = 'Sample Annotation Type'
COLLECTION = 'Sample Collection'
COLLECTION_TYPE = 'Sample Collection Type'
DEVICE_BRAND = 'Sample Device Brand'
DEVICE_MODEL = 'Sample Device Model'
DEVICE_SERIAL_NUMBER = '123456789'
DEVICE_TYPE = 'Sample Device Type'
EVENT_TYPE = 'Sample Event Type'
INSTITUTION = 'Sample Institution'
ITEM_HASH = 'sampleitemhash'
ITEM_MIME = 'audio/x-wav'
ITEM_PATH = '/sample/path/to/item.wav'
ITEM_TYPE = 'Sample Item Type'
ITEM_TYPE = 'Sample Item Type'
LICENCE_TYPE = 'Sample Licence Type'
METACOLLECTION = 'Sample Meta Collection'
PARSE_FUNCTION = 'sample_parse_function'
ROLE = 'Sample Role'
SAMPLING_EVENT_TYPE = 'Sample Sampling Event Type'
SECONDARY_ITEM_HASH = 'samplehashofsecondaryitem'
SECONDARY_ITEM_PATH = '/sample/path/to/secondary/item.wav'
SITE = 'Sample Site'
SITE_TYPE = 'Sample Site Type'
SITE_TYPE = 'Sample Site Type'
SOURCE_DIRECTORY = '/sample/source/directory/'
SOURCE_FILE = 'sample_source_file.csv'
TERM_TYPE = 'Sample Term Type'
TERM_VALUE = 'Sample Term Value'
USER_NAME = 'sampleuser'
USER_PASSWORD = 'sampleuser'
USER_EMAIL = 'sampleuser@sample.domain.com'
USER_FIRST_NAME = 'Sample User'


SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "title": "Sample Schema",
    "required": [
        "sample_required_parameter"
    ],
    "properties": {
        "sample_parameter": {
            "type": "string",
        },
        "sample_required_parameter": {
            "type": "integer",
        }
    }
}
VALID_INSTANCE = {'sample_required_parameter': 1}
INVALID_INSTANCE = {'sample_parameter': "a"}


SAMPLE_ANNOTATION_SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "title": "BBox Annotation",
    "required": [
        "x",
        "y",
        "height",
        "width"
    ],
    "properties": {
        "x": {
            "type": "integer"
        },
        "y": {
            "type": "integer"
        },
        "height": {
            "type": "integer",
        },
        "width": {
            "type": "integer",
        }
    }
}
VALID_ANNOTATION = {
    'x': 10,
    'y': 20,
    'height': 100,
    'width': 100
}
INVALID_ANNOTATION = {
    'x': 10
}


ANNOTATION_TOOL_CONFIGURATION_SCHEMA = Schema(
    name='Sample Annotation Tool Configuration Schema',
    schema=SCHEMA)
ANNOTATION_SCHEMA = Schema(
    name='Sample Annotation Schema',
    schema=SAMPLE_ANNOTATION_SCHEMA)
DEVICE_METADATA_SCHEMA = Schema(
    name='Sample Device Metadata Schema',
    schema=SCHEMA)
COLLECTION_ITEM_TYPE_METADATA_SCHEMA = Schema(
    name='Sample Item Type Metadata Schema',
    schema=SCHEMA)
COLLECTION_ROLE_METADATA_SCHEMA = Schema(
    name='Sample Role Metadata Schema',
    schema=SCHEMA)
COLLECTION_TYPE_METADATA_SCHEMA = Schema(
    name='Sample Type Metadata Schema',
    schema=SCHEMA)
DEVICE_METADATA_SCHEMA = Schema(
    name='Sample Device Metadata Schema',
    schema=SCHEMA)
DEVICE_CONFIGURATION_SCHEMA = Schema(
    name='Sample Device Configuration Schema',
    schema=SCHEMA)
MEDIA_INFO_SCHEMA = Schema(
    name='Sample Media Info Schema',
    schema=SCHEMA)
LICENCE_METADATA_SCHEMA = Schema(
    name='Sample Licence Metadata Schema',
    schema=SCHEMA)
SAMPLING_EVENT_METADATA_SCHEMA = Schema(
    name='Sample Sampling Event Metadata Schema',
    schema=SCHEMA)
SITE_METADATA_SCHEMA = Schema(
    name='Sample Site Metadata Schema',
    schema=SCHEMA)
TERM_METADATA_SCHEMA = Schema(
    name='Sample Term Metadata Schema',
    schema=SCHEMA)
SYNONYM_METADATA_SCHEMA = Schema(
    name='Sample Synonym Metadata Schema',
    schema=SCHEMA)
