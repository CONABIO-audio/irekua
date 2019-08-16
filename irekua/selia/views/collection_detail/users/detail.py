from django.views.generic.detail import SingleObjectMixin
from django import forms

from database.models import CollectionUser
from selia.views.utils import SeliaDetailView
from selia.forms.json_field import JsonField

from database.models import SamplingEvent
from database.models import CollectionSite
from database.models import CollectionDevice
from database.models import Item
from database.models import Annotation


class CollectionUserUpdateForm(forms.ModelForm):
    metadata = JsonField()

    class Meta:
        model = CollectionUser
        fields = [
            'role',
            'metadata',
        ]


class CollectionUserDetailView(SeliaDetailView, SingleObjectMixin):
    model = CollectionUser
    form_class = CollectionUserUpdateForm
    delete_redirect_url = 'selia:collection_users'

    template_name = 'selia/collection_detail/users/detail.html'
    help_template = 'selia/components/help/collection_user_detail.html'
    detail_template = 'selia/components/details/collection_user.html'
    summary_template = 'selia/components/summaries/collection_user.html'
    update_form_template = 'selia/components/update/collection_user.html'
    viewer_template = 'selia/components/viewers/collection_user.html'

    def get_delete_redirect_url_args(self):
        return [self.object.collection.pk]

    def get_summary_info(self):
        user = self.object.user
        collection = self.object.collection

        sampling_events = (
            SamplingEvent.objects
            .filter(collection=collection, created_by=user)
            .count())
        collection_sites = (
            CollectionSite.objects
            .filter(collection=collection, created_by=user)
            .count())
        collection_devices = (
            CollectionDevice.objects
            .filter(collection=collection, created_by=user)
            .count())
        items = (
            Item.objects
            .filter(
                sampling_event_device__sampling_event__collection=collection,
                created_by=user)
            .count())
        annotations = (
            Annotation.objects
            .filter(
                item__sampling_event_device__sampling_event__collection=collection,
                created_by=user)
            .count())

        return {
            'sampling_events': sampling_events,
            'collection_sites': collection_sites,
            'collection_devices': collection_devices,
            'items': items,
            'annotations': annotations,
        }

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['collection'] = self.object.collection
        context['summary_info'] = self.get_summary_info()
        return context
