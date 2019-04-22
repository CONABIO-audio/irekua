from django.urls import reverse
from rest_framework import serializers


__all__ = ['ModelTable']


class ModelTable(serializers.ModelSerializer):
    with_link = False

    def __init__(self, *args, **kwargs):
        self.pre_args = kwargs.pop('pre_args', [])
        self.post_args = kwargs.pop('post_args', [])
        super().__init__(*args, **kwargs)

    def get_object_url(self, datum):
        if not self.url_args:
            raise ValueError

        if not self.detail_view:
            raise ValueError

        args = (
            self.pre_args +
            [datum[key] for key in self.url_args] +
            self.post_args)
        return reverse(self.detail_view, args=args)
