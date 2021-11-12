from geonode.goos.models import Eov
from rest_framework import viewsets
from geonode.goos.api.serializers import EovSerializer


class EovViewSet(viewsets.ModelViewSet):
    queryset = Eov.objects.all()
    serializer_class = EovSerializer
