from django.urls import path
from selia.views import autocomplete


urlpatterns = [
    path(
        'autocomplete/institutions/',
        autocomplete.InstitutionAutocomplete.as_view(),
        name='institutions_autocomplete'),
    path(
        'autocomplete/device_brands/',
        autocomplete.DeviceBrandAutocomplete.as_view(create_field="name"),
        name='device_brands_autocomplete'),
    path(
        'autocomplete/devices/',
        autocomplete.DeviceAutocomplete.as_view(),
        name='devices_autocomplete'),
    path(
        'autocomplete/collections/',
        autocomplete.CollectionAutocomplete.as_view(),
        name='collection_autocomplete'),
    path(
        'autocomplete/collection_types/',
        autocomplete.CollectionTypeAutocomplete.as_view(),
        name='collection_type_autocomplete'),
    path(
        'autocomplete/metacollections/',
        autocomplete.MetacollectionAutocomplete.as_view(),
        name='metacollection_autocomplete'),
    path(
        'autocomplete/terms/',
        autocomplete.TermsAutocomplete.as_view(),
        name='terms_autocomplete'),
    path(
        'autocomplete/tags/',
        autocomplete.TagsAutocomplete.as_view(),
        name='tags_autocomplete'),
    path(
        'autocomplete/annotation_tools/',
        autocomplete.AnnotationToolsAutocomplete.as_view(),
        name='annotation_tools_autocomplete'),
    path(
        'autocomplete/sampling_event_types/',
        autocomplete.SamplingEventTypesAutocomplete.as_view(),
        name='sampling_event_types_autocomplete'),
    path(
        'autocomplete/users/',
        autocomplete.UserAutocomplete.as_view(),
        name='users_autocomplete'),
]
