"""irekua URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from rest_framework.documentation import include_docs_urls


urlpatterns = [
    url(r'^admin/docs/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^api/v1/', include(('rest.urls', 'rest-api'), namespace='v1')),
    url(r'^api/v1/docs/', include_docs_urls(title='Irekua REST API documentation')),
    url(r'^api/auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'', include(('selia.urls', 'selia'))),
    url(r'^registration/', include(('registration.urls', 'registration'))),
    url(r'^file_handling/', include(('file_handler.urls', 'file_handler'))),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
