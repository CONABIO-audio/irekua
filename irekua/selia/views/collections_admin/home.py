from django.views.generic import TemplateView
from django.core.paginator import Paginator


class Home(TemplateView):
    template_name = 'selia/collections_admin/home.html'

    @staticmethod
    def paginate_collections(queryset):
        paginator = Paginator(queryset, 5)
        return paginator.get_page(1)

    def get_paginated_collection_types(self):
        user = self.request.user
        paginated_collections = [
            (
                collection_type,
                self.paginate_collections(collection_type.collection_set.all())
            )
            for collection_type in user.collectiontype_set.all()
        ]

        return paginated_collections

    def get_context_data(self):
        collection_types = self.get_paginated_collection_types()
        return {'collection_types': collection_types}
