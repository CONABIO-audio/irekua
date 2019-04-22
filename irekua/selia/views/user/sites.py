from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from database.models import Site
from selia.utils import ModelTable


class SiteTable(ModelTable):
    class Meta:
        model = Site
        fields = ['id', 'name', 'locality']


@login_required(login_url='registration:login')
def user_sites(request):
    user = request.user
    sites = user.site_set.all()

    table = SiteTable(sites, many=True)
    context = {'table': table}
    return render(request, 'selia/user/sites.html', context)
