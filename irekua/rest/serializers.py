from rest_framework import serializers
import database.models as db


class ItemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = db.Item
