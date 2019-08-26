import uuid
from django.core.mail import send_mail
from django.urls import reverse
from django.utils.translation import gettext as _
from django.conf import settings

from selia.views.utils import SeliaCreateView
from database.models import User


LENGTH = 12

SUBJECT = _(
    'Invitation to join Selia'
)

MESSAGE = _(
    'Hi!\n'
    'You have been invited to join Selia by %(inviter)s! '
    'A temporal password has been created for you. To access your temporal account '
    'please enter the following site %(url)s with the info provided.\n\n'
    'PASSWORD: %(password)s\n'
    'USERNAME: %(username)s\n\n'
    'Cheers!\n'
    'The Selia team'
)


class CreateUserView(SeliaCreateView):
    template_name = 'selia/create/users/create_form.html'
    success_url = 'selia:user_home'

    model = User
    fields = [
        'email',
    ]

    def get_additional_query_on_sucess(self):
        return {
            'user': self.object.pk,
        }

    def send_invitation_email(self, user):
        message = MESSAGE.format(
            inviter=self.request.user.username,
            password=user.password,
            username=user.username,
            url=reverse('registration:login'))

        send_mail(
            SUBJECT,
            message,
            settings.EMAIL,
            [user.email],
            fail_silently=True)


    def save_form(self, form):
        user = form.save(commit=False)
        user.password = uuid.uuid4().hex.lower()[0:LENGTH]
        user.username = form.cleaned_data['email'].split('@')[0]
        user.save()
        self.send_invitation_email(user)
        return user
