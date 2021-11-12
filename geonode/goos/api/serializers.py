from geonode.goos.models import Eov
from rest_framework import serializers


class EovSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Eov
        fields = ['id', 'name', 'short_name', 'description', 'url']