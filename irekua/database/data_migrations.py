from django.db import migrations
from importlib import import_module
from database.utils import FREE_SCHEMA


def create_basic_json_schema(apps, schema_editor):
    free_schema = {
      "definitions": {},
      "$schema": "http://json-schema.org/draft-07/schema#",
      "type": "object",
      "title": "Free JSON Schema"
    }

    Schema = apps.get_model('database', 'Schema')
    Schema.objects.get_or_create(
        field='global',
        name=FREE_SCHEMA,
        description='JSON Schema with no restrictions',
        schema=free_schema)


def create_basic_roles(apps, schema_editor):
    from database.defaults.role_types import types

    RoleType = apps.get_model('database', 'RoleType')
    Permission = apps.get_model('auth', 'Permission')

    for role_type in types:
        group, created = RoleType.objects.get_or_create(
            name=role_type['name'],
            description=role_type['description'])

        for permission_code in role_type['permissions']:
            permission = Permission.objects.get(codename=permission_code)
            group.permissions.add(permission)


def create_basic_types(submodule, model, schema_fields=None):
    def create_function(apps, schema_editor):
        module = import_module(submodule)
        types = module.types

        Schema = apps.get_model('database', 'Schema')
        Model = apps.get_model('database', model)

        for type_info in types:
            field_values = {}

            for field_name in type_info:
                if not isinstance(type_info[field_name], dict):
                    field_values[field_name] = type_info[field_name]
                    continue

                schema = type_info[field_name]

                schema_name = schema['title']
                schema_description = schema['description']

                schema, created = Schema.objects.get_or_create(
                    field=schema_fields[field_name],
                    name=schema_name,
                    description=schema_description,
                    schema=schema)
                field_values[field_name] = schema

            Model.objects.get_or_create(**field_values)

    return create_function


def create_basic_item_types(apps, schema_editor):
    from database.defaults.item_types import types

    Schema = apps.get_model('database', 'Schema')
    ItemType = apps.get_model('database', 'ItemType')

    for item_type in types:
        name = item_type['name']
        description = item_type['description']
        schema = item_type['schema']

        schema, created = Schema.objects.get_or_create(
            field='item_media_info',
            name='{} media info'.format(name),
            description=schema.get('description', ''),
            schema=schema)

        ItemType.objects.get_or_create(
            name=name,
            description=description,
            media_info_schema=schema)


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
        ('contenttypes', '0002_remove_content_type_name'),
        ('database', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_basic_json_schema),
        migrations.RunPython(create_basic_roles),
        migrations.RunPython(
            create_basic_types(
                'database.defaults.item_types',
                'ItemType',
                {'media_info_schema': 'item_media_info'})),
        migrations.RunPython(
            create_basic_types(
                'database.defaults.annotation_types',
                'AnnotationType',
                {'schema': 'annotation'})),
        migrations.RunPython(
            create_basic_types(
                'database.defaults.device_types',
                'DeviceType')),
        migrations.RunPython(
            create_basic_types(
                'database.defaults.licence_types',
                'LicenceType',
                {'metadata_schema': 'licence_metadata'})),
        migrations.RunPython(
            create_basic_types(
                'database.defaults.site_types',
                'SiteType',
                {'metadata_schema': 'site_metadata'})),
        migrations.RunPython(
            create_basic_types(
                'database.defaults.term_types',
                'TermType',
                {
                    'metadata_schema': 'term_metadata',
                    'synonym_metadata_schema': 'synonym_metadata',
                })),
    ]
