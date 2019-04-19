from django.urls import path
from django.urls import include
from django.urls import re_path
from django.contrib.auth import views as auth_views


urlpatterns = [
    path(
        'accounts/',
        include('django.contrib.auth.urls')
    ),
    path(
        'password_reset/',
        auth_views.PasswordResetView.as_view(),
        {'template_name': 'registration/Reset_email.html'},
        name='password_reset'
    ),
    path(
        'password_reset/done/',
        auth_views.PasswordResetDoneView.as_view(),
        {'template_name': 'registration/Reset_Email_Sent.html'},
        name='password_reset_done'
    ),
    re_path(
        r'reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',
        auth_views.PasswordResetConfirmView.as_view(),
        {'template_name': 'registration/Forgot_password.html'},
        name='password_reset_confirm'
    ),
    path(
        'reset/done/',
        auth_views.PasswordResetCompleteView.as_view(),
        {'template_name': 'registration/Signin.html'},
        name='password_reset_complete'
    )
]
