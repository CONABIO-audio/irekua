from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from database.models import Collection
from selia.utils import ModelTable


class CollectionTable(ModelTable):
    class Meta:
        model = Collection
        fields = ['name', 'created_on', 'logo']


@login_required(login_url='registration:login')
def user_collections(request):
    user = request.user
    collections = user.collection_users.all()

    table = CollectionTable(collections, many=True)
    context = {'table': table}
    return render(request, 'selia/user/collections.html', context)
