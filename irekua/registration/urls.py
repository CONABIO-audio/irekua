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
        auth_views.PasswordResetView.as_view(
            template_name='selia/password_reset_form.html',
            email_template_name='selia/password_reset_email.html',
            subject_template_name='selia/password_reset_subject.txt',
            success_url='done'),
        name='password_reset'
    ),
    path(
        'password_reset/done/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='selia/password_reset_done.html'),
        name='password_reset_done'
    ),
    re_path(
        r'reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='selia/password_reset_confirm.html'),
        name='password_reset_confirm'
    ),
    path(
        'reset/done/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='selia/password_reset_complete.html'),
        name='password_reset_complete'
    )
]
