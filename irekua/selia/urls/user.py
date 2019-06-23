from django.urls import path
from selia.views import user


urlpatterns = [
    path('user/', user.user_home, name='user_home'),
]
