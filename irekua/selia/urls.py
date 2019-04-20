from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('user/', views.user_home, name='user_home'),
    path('about/', views.about, name='about'),
]
