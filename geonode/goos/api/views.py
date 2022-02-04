from rest_framework import viewsets, serializers
from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet
from geonode.base.models import ThesaurusKeyword
from rest_framework.permissions import AllowAny


class EovKeywordSerializer(serializers.ModelSerializer):

    class Meta:
        model = ThesaurusKeyword
        fields = ["id", "about", "alt_label"]


class EovKeywordViewSet(ListModelMixin, GenericViewSet):
    permission_classes = [AllowAny, ]
    queryset = ThesaurusKeyword.objects.all().filter(about__icontains="goos")
    serializer_class = EovKeywordSerializer
