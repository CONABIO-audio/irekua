from selia.views.utils import SeliaCreateView
from database.models import Collection
from database.models import Licence
from database.models import LicenceType


class CollectionLicenceCreateView(SeliaCreateView):
    template_name = 'selia/collection_detail/licences/create.html'
    model = Licence
    success_url = 'selia:collection_licences'
    fields = [
        'licence_type',
        'document',
        'metadata',
        'collection',
    ]

    def get_success_url_args(self):
        return [self.kwargs['pk']]

    def handle_create(self):
        form = self.get_form()
        if form.is_valid():
            licence = form.save(commit=False)
            licence.created_by = self.request.user
            licence.save()
            return self.handle_finish_create()
        else:
            self.object = None
            context = self.get_context_data()
            context['form'] = form
            return self.render_to_response(context)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        collection = self.get_object(queryset=Collection.objects.all())
        context['collection'] = collection

        collection_type = collection.collection_type
        if collection_type.restrict_licence_types:
            context['licence_types'] = collection_type.licence_types.all()
        else:
            context['licence_types'] = LicenceType.objects.all()

        if 'licence_type' in self.request.GET:
            licence_type = LicenceType.objects.get(pk=self.request.GET['licence_type'])
            context['licence_type'] = licence_type
        return context
