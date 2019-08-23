from django.views.generic import TemplateView
from django.shortcuts import redirect
from django.urls import reverse

from database.models import Collection
from database.models import SiteType


class SelectCollectionSiteTypeView(TemplateView):
    template_name = 'selia/create/collection_sites/select_type.html'

    def should_redirect(self):
        self.collection = Collection.objects.get(pk=self.request.GET['collection'])

        collection_type = self.collection.collection_type

        if collection_type.restrict_site_types:
            self.site_types = collection_type.site_types.all()
        else:
            self.site_types = SiteType.objects.all()

        return self.site_types.count() == 1

    def handle_single_type_redirect(self):
        url = reverse('selia:create_collection_site')
        full_url = '{url}?{query}&site_type={pk}'.format(
            url=url,
            query=self.request.GET.urlencode(),
            pk=self.site_types.first().pk)
        return redirect(full_url)

    def get(self, *args, **kwargs):
        if self.should_redirect():
            return self.handle_single_type_redirect()

        return super().get(*args, **kwargs)

    def get_context_data(self):
        context = super().get_context_data()
        context['collection'] = self.collection
        context['list'] = self.site_types
        return context
