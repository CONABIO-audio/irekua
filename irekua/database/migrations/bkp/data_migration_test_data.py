from django.db import migrations
from database import models
from database.utils import simple_JSON_schema

from random import random, choice, sample
import datetime
from django.utils import timezone


def make_test_data(apps, schema_editor):
    CONABIO, _ = models.Institution.objects.get_or_create(
        institution_name='CONABIO',
        institution_code='CONABIO',
        subdependency='DGPI',
        country='MX')

    CONANP, _ = models.Institution.objects.get_or_create(
        institution_name='CONANP',
        institution_code='CONANP',
        subdependency='PROCER',
        country='MX')

    conanp_admin = models.User.objects.create_user(
        username='conanp_admin',
        first_name='conanp',
        last_name='admin',
        password='conanpadmin',
        email='1@gmail.com',
        institution=CONANP)
    conanp_user_1 = models.User.objects.create_user(
        username='conanp_user_1',
        first_name='conanp',
        last_name='usuario uno',
        password='conanpuser',
        email='2@gmail.com',
        institution=CONANP)
    conanp_user_2 = models.User.objects.create_user(
        username='conanp_user_2',
        first_name='conanp',
        last_name='usuario dos',
        password='conanpuser',
        email='3@gmail.com',
        institution=CONANP)
    conanp_user_3 = models.User.objects.create_user(
        username='conanp_user_3',
        first_name='conanp',
        last_name='usuario tres',
        password='conanpuser',
        email='4@gmail.com',
        institution=CONANP)
    conabio_admin = models.User.objects.create_user(
        username='conabio_admin',
        first_name='conabio',
        last_name='admin',
        password='conabioadmin',
        email='5@gmail.com',
        institution=CONABIO,
        is_superuser=True)

    term_type_species, _ = models.TermType.objects.get_or_create(
        name='especie',
        description='Nombre cientifico',
        is_categorical=True,
        metadata_schema=simple_JSON_schema(),
        synonym_metadata_schema=simple_JSON_schema())
    term_type_genus, _ = models.TermType.objects.get_or_create(
        name='genero',
        description='Genero taxonómico',
        is_categorical=True,
        metadata_schema=simple_JSON_schema(),
        synonym_metadata_schema=simple_JSON_schema())

    procer_site, _ = models.SiteType.objects.get_or_create(
        name='Sitio Procer',
        description='Tipo de sitio utilizado en colectas procer',
        metadata_schema=simple_JSON_schema())

    open_licence_type, _ = models.LicenceType.objects.get_or_create(
        name='Licencia Abierta',
        description='Licencia que permite el uso libre',
        metadata_schema=simple_JSON_schema(),
        years_valid_for=9999,
        can_view=True,
        can_download=True,
        can_view_annotations=True,
        can_annotate=True,
        can_vote_annotations=True)
    restricted_licence_type, _ = models.LicenceType.objects.get_or_create(
        name='Licencia con restricciones',
        description='Licencia que restringe el acceso',
        metadata_schema=simple_JSON_schema(),
        years_valid_for=3,
        can_view=False,
        can_download=False,
        can_view_annotations=False,
        can_annotate=False,
        can_vote_annotations=False)

    animal_in_photo, _ = models.EventType.objects.get_or_create(
        name='Animal en Foto',
        description='Ocurrencia de animal en una fotografía')
    animal_in_photo.term_types.set([term_type_species, term_type_genus])

    png_mime_type, _ = models.MimeType.objects.get_or_create(
        media_info_schema=simple_JSON_schema(),
        mime_type='image/png')
    jpg_mime_type, _ = models.MimeType.objects.get_or_create(
        media_info_schema=simple_JSON_schema(),
        mime_type='image/jpeg')

    camera_trap_item, _ = models.ItemType.objects.get_or_create(
        name='Foto de Camara Trampa',
        description='Foto en formato png tomada con camara trampa')

    camera_trap_item.mime_types.add(png_mime_type, jpg_mime_type)
    camera_trap_item.event_types.set([animal_in_photo])

    camera, _ = models.DeviceType.objects.get_or_create(
        name='camara',
        description='Camara')

    bbox, _ = models.AnnotationType.objects.get_or_create(
        name='Bounding Box',
        description='Anotación de bounding box',
        annotation_schema=simple_JSON_schema())

    regular_user, _ = models.Role.objects.get_or_create(
        name='Usuario Regular',
        description='Usuario regular de la colección')
    regular_user.add_permission_from_codename([
        "add_collection_site",
        "add_collection_item",
        "add_collection_annotation",
        "add_collection_annotation_vote",
        "view_collection_sites",
        "view_collection_items",
        "view_collection_devices",
        "view_collection_sampling_events",
        "view_collection_annotations",
        "download_collection_items",
    ])
    collection_admin, _ = models.Role.objects.get_or_create(
        name='Administrador',
        description='Administrador de colección')
    collection_admin.add_permission_from_codename([
        "add_collection_site",
        "add_collection_item",
        "add_collection_annotation",
        "add_collection_annotation_vote",
        "add_collection_user",
        "add_collection_licence",
        "view_collection_sites",
        "view_collection_items",
        "view_collection_devices",
        "view_collection_sampling_events",
        "view_collection_annotations",
        "download_collection_items",
        "change_collection_sites",
        "change_collection_users",
        "change_collection_items",
        "change_collection_annotations",
        "change_collection_sampling_events",
    ])

    procer_sampling, _ = models.SamplingEventType.objects.get_or_create(
        name='Evento de Muestreo Procer',
        description='Evento de muestreo Procer',
        metadata_schema=simple_JSON_schema(),
        restrict_device_types=True,
        restrict_site_types=True)
    procer_sampling.add_device_type(camera, simple_JSON_schema())
    procer_sampling.site_types.set([procer_site])

    procer_collection_type, _ = models.CollectionType.objects.get_or_create(
        name='Procer',
        description='Colección tipo procer',
        metadata_schema=simple_JSON_schema(),
        anyone_can_create=False,
        restrict_site_types=True,
        restrict_annotation_types=True,
        restrict_item_types=True,
        restrict_licence_types=True,
        restrict_device_types=True,
        restrict_event_types=True,
        restrict_sampling_event_types=True)
    procer_collection_type.add_site_type(procer_site)
    procer_collection_type.add_item_type(camera_trap_item)
    procer_collection_type.add_annotation_type(bbox)
    procer_collection_type.add_device_type(camera)
    procer_collection_type.add_licence_type(open_licence_type)
    procer_collection_type.add_event_type(animal_in_photo)
    procer_collection_type.add_sampling_event_type(procer_sampling)
    procer_collection_type.add_administrator(conanp_admin)
    procer_collection_type.add_role(regular_user)
    procer_collection_type.add_role(collection_admin)

    procer_collection, _ = models.Collection.objects.get_or_create(
        collection_type=procer_collection_type,
        name='Colección Procer 1',
        description='Colección procer 1',
        metadata={},
        institution=CONANP,
        is_open=True)

    procer_collection.administrators.add(conanp_user_1)
    procer_collection.add_user(conanp_user_1, collection_admin, {})
    procer_collection.add_user(conanp_user_2, regular_user, {})
    procer_collection.add_user(conanp_user_3, regular_user, {})

    device_brand_1, _ = models.DeviceBrand.objects.get_or_create(
        name="Browning")
    device_brand_2, _ = models.DeviceBrand.objects.get_or_create(
        name="Skypoint")
    device_1, _ = models.Device.objects.get_or_create(
        device_type=camera,
        brand=device_brand_1,
        model="Strike Force Pro XD",
        metadata_schema=simple_JSON_schema(),
        configuration_schema=simple_JSON_schema())
    device_2, _ = models.Device.objects.get_or_create(
        device_type=camera,
        brand=device_brand_2,
        model="Solar",
        metadata_schema=simple_JSON_schema(),
        configuration_schema=simple_JSON_schema())

    index = 0
    for user in [conanp_user_1, conanp_user_2, conanp_user_3]:
        index += 1
        for n in range(9):
            site, _ = models.Site.objects.get_or_create(
                name="Sitio {}".format(index * 10 + n),
                latitude=10 * random(),
                longitude=10 * random(),
                created_by=user)
            device, _ = models.PhysicalDevice.objects.get_or_create(
                serial_number=int(10000 * random()),
                device=choice([device_1, device_2]),
                created_by=user,
                metadata={},
                bundle=False)
            procer_collection.add_site(site, index * 10 + n,
                site_type=procer_site, metadata={})
            procer_collection.add_device(device, index * 10 + n, {})

    collection_sites = procer_collection.collectionsite_set.all()
    collection_devices = procer_collection.collectiondevice_set.all()
    for site in collection_sites:
        timedelta1 = datetime.timedelta(days=int(400 * random()))
        timedelta2 = datetime.timedelta(days=int(60 * random()))
        start = timezone.now() - timedelta1 - timedelta2
        end = timezone.datetime.now() - timedelta1

        sampling_event, _ = models.SamplingEvent.objects.get_or_create(
            sampling_event_type=procer_sampling,
            collection_site=site,
            metadata={},
            started_on=start,
            ended_on=end,
            collection=procer_collection,
            created_by=site.site.created_by)

        devices = sample(list(collection_devices), 4)
        for device in devices:
            models.SamplingEventDevice.objects.get_or_create(
                sampling_event=sampling_event,
                collection_device=device,
                metadata={},
                configuration={},
                created_by=device.physical_device.created_by)


class Migration(migrations.Migration):
    dependencies = [
        ('database', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(make_test_data)
    ]
