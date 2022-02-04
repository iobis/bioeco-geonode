from rest_framework import viewsets, serializers
from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet
from geonode.base.models import ThesaurusKeyword
from rest_framework.permissions import AllowAny


class FastThesaurusKeywordSerializer(serializers.ModelSerializer):

    class Meta:
        model = ThesaurusKeyword
        #name = 'tkeywords'
        #view_name = 'tkeywords-list'
        fields = '__all__'


class FastThesaurusKeywordViewSet(ListModelMixin, GenericViewSet):
    permission_classes = [AllowAny, ]
    queryset = ThesaurusKeyword.objects.all()
    serializer_class = FastThesaurusKeywordSerializer
