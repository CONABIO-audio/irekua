from rest_framework import serializers
from django.contrib.auth.models import Permission
import database.models as db


class InstitutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = db.Institution
        fields = (
            'institution_name',
            'institution_code',
            'subdependency',
            'country',
            'postal_code',
            'address',
            'website',
            'logo',
        )


class UserSerializer(serializers.ModelSerializer):
    institution = InstitutionSerializer(many=False, read_only=False)

    class Meta:
        model = db.User
        fields = (
            'username',
            'email',
            'password',
            'first_name',
            'last_name',
            'institution',
        )


class TermSerializer(serializers.ModelSerializer):
    class Meta:
        model = db.Term
        fields = (
            'value',
            'description',
            'metadata',
            'term_type'
        )


class TermTypeSerializer(serializers.ModelSerializer):
    term_set = TermSerializer(many=True, read_only=False)

    class Meta:
        model = db.TermType
        fields = (
            'name',
            'description',
            'icon',
            'is_categorical',
            'metadata_schema',
            'synonym_metadata_schema',
            'term_set',
        )


class LicenceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = db.LicenceType
        fields = (
            'name',
            'description',
            'metadata_schema',
            'document_template',
            'years_valid_for',
            'icon',
            'can_view',
            'can_download',
            'can_view_annotations',
            'can_annotate',
            'can_vote_annotations',
        )


class EventTypeSerializer(serializers.HyperlinkedModelSerializer):
    term_types = TermTypeSerializer(many=True, read_only=False)

    class Meta:
        model = db.EventType
        fields = (
            'name',
            'description',
            'icon',
            'term_types',
        )


class ItemTypeSerializer(serializers.ModelSerializer):
    event_types = EventTypeSerializer(many=True, read_only=False)

    class Meta:
        model = db.ItemType
        fields = (
            'name',
            'description',
            'media_info_schema',
            'media_type',
            'icon',
            'event_types',
        )


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = db.Tag
        fields = (
            'name',
            'description',
            'icon'
        )


class SiteTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = db.SiteType
        fields = (
            'name',
            'description',
            'metadata_schema'
        )


class SiteSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(many=False, read_only=False)
    site_type = SiteTypeSerializer(many=False, read_only=False)

    class Meta:
        model = db.Site
        fields = (
            'name',
            'locality',
            'site_type',
            'latitude',
            'longitude',
            'altitude',
            'metadata',
            'created_by',
        )


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = (
            'content_type',
            'codename'
        )


class RoleSerializer(serializers.HyperlinkedModelSerializer):
    permissions = PermissionSerializer(many=True, read_only=False)

    class Meta:
        model = db.Role
        fields = (
            'name',
            'description',
            'permissions',
            'icon',
        )

class CollectionUserSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False, read_only=False)
    role = RoleSerializer(many=False, read_only=False)

    class Meta:
        model = db.CollectionUser
        fields = (
            'user',
            'role',
            'metadata',
            'collection',
        )


class CollectionSiteSerializer(serializers.ModelSerializer):
    site = SiteSerializer(many=False, read_only=False)

    class Meta:
        model = db.CollectionSite
        fields = (
            'site',
            'internal_id',
            'collection',
        )


class DeviceTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = db.DeviceType
        fields = (
            'name',
            'description',
            'icon',
        )


class DeviceBrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = db.DeviceBrand
        fields = (
            'name',
            'website',
            'logo',
        )


class DeviceSerializer(serializers.ModelSerializer):
    device_type = DeviceTypeSerializer(many=False, read_only=False)
    brand = DeviceBrandSerializer(many=False, read_only=False)

    class Meta:
        model = db.Device
        fields = (
            'device_type',
            'brand',
            'model',
            'metadata_schema',
            'configuration_schema',
        )


class PhysicalDeviceSerializer(serializers.ModelSerializer):
    owner = UserSerializer(many=False, read_only=False)
    device = DeviceSerializer(many=False, read_only=False)

    class Meta:
        model = db.PhysicalDevice
        fields = (
            'serial_number',
            'device',
            'metadata',
            'bundle',
            'owner',
        )


class CollectionDevicesSerializer(serializers.ModelSerializer):
    physical_device = PhysicalDeviceSerializer(many=False, read_only=False)

    class Meta:
        model = db.CollectionDevice
        fields = (
            'physical_device',
            'metadata',
            'internal_id',
            'collection'
        )


class SamplingEventTypeSerializer(serializers.ModelSerializer):
    site_types = SiteTypeSerializer(many=True, read_only=False)
    device_types = DeviceTypeSerializer(many=True, read_only=False)

    class Meta:
        model = db.SamplingEventType
        fields = (
            'name',
            'description',
            'icon',
            'metadata_schema',
            'restrict_device_types',
            'restrict_site_types',
            'device_types',
            'site_types',
        )


class AnnotationTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = db.AnnotationType
        fields = (
            'name',
            'description',
            'annotation_schema',
            'icon',
        )


class CollectionTypeSerializer(serializers.ModelSerializer):
    site_types = SiteTypeSerializer(many=True, read_only=False)
    annotation_types = AnnotationTypeSerializer(many=True, read_only=False)
    item_types = ItemTypeSerializer(many=True, read_only=False)
    licence_types = LicenceTypeSerializer(many=True, read_only=False)
    device_types = DeviceTypeSerializer(many=True, read_only=False)
    event_types = EventTypeSerializer(many=True, read_only=False)
    sampling_event_types = SamplingEventTypeSerializer(many=True, read_only=False)
    roles = RoleSerializer(many=True, read_only=False)
    administrators = UserSerializer(many=True, read_only=False)

    class Meta:
        model = db.CollectionType
        fields = (
            'name',
            'logo',
            'description',
            'metadata_schema',
            'anyone_can_create',
            'restrict_site_types',
            'restrict_annotation_types',
            'restrict_item_types',
            'restrict_licence_types',
            'restrict_device_types',
            'restrict_event_types',
            'restrict_sampling_event_types',
            'site_types',
            'annotation_types',
            'item_types',
            'licence_types',
            'device_types',
            'event_types',
            'sampling_event_types',
            'roles',
            'administrators',
        )



class CollectionSerializer(serializers.ModelSerializer):
    institution = InstitutionSerializer(many=False, read_only=False)
    users = CollectionUserSerializer(many=True, read_only=False)
    sites = CollectionSiteSerializer(many=True, read_only=False)
    physical_devices = CollectionDevicesSerializer(many=True, read_only=False)
    collection_type = CollectionTypeSerializer(many=False, read_only=False)

    class Meta:
        model = db.Collection
        fields = (
            'name',
            'collection_type',
            'description',
            'logo',
            'metadata',
            'institution',
            'physical_devices',
            'users',
            'sites',
        )


class LicenceSerializer(serializers.ModelSerializer):
    signed_by = UserSerializer(many=False, read_only=False)
    licence_type = LicenceTypeSerializer(many=False, read_only=False)
    collection = CollectionSerializer(many=False, read_only=False)

    class Meta:
        model = db.Licence
        fields = (
            'licence_type',
            'document',
            'metadata',
            'collection',
            'signed_by',
        )


class SamplingEventSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(many=False, read_only=False)
    licence = LicenceSerializer(many=False, read_only=False)
    sampling_event_type = SamplingEventTypeSerializer(many=False, read_only=False)
    site = SiteSerializer(many=False, read_only=False)

    class Meta:
        model = db.SamplingEvent
        fields = (
            'sampling_event_type',
            'site',
            'physical_device',
            'configuration',
            'commentaries',
            'metadata',
            'started_on',
            'ended_on',
            'licence',
            'created_by',
            'collection',
        )


class ItemSerializer(serializers.ModelSerializer):
    item_type = ItemTypeSerializer(many=False, read_only=False)
    licence = LicenceSerializer(many=False, read_only=False)
    tags = TagSerializer(many=True, read_only=False)
    ready_event_types = EventTypeSerializer(many=True, read_only=False)
    sampling_event = SamplingEventSerializer(many=False, read_only=False)

    class Meta:
        model = db.Item
        fields = (
            'hash',
            'item_file',
            'item_type',
            'media_info',
            'metadata',
            'captured_on',
            'licence',
            'sampling_event',
            'tags',
            'source',
            'source_foreign_key',
            'ready_event_types',
        )
