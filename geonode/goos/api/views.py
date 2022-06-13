from rest_framework import viewsets, serializers
from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet
from geonode.base.models import ThesaurusKeyword
from rest_framework.permissions import AllowAny
from dynamic_rest.filters import BaseFilterBackend
from dynamic_rest.serializers import DynamicModelSerializer
from dynamic_rest.viewsets import DynamicModelViewSet
from geonode.layers.models import Layer
from dynamic_rest.filters import DynamicFilterBackend, DynamicSortingFilter
from geonode.base.api.filters import DynamicSearchFilter, ExtentFilter
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from geonode.base.api.permissions import IsOwnerOrReadOnly
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from oauth2_provider.contrib.rest_framework import OAuth2Authentication
from geonode.base.api.pagination import GeoNodeApiPagination
from geonode.layers.api.permissions import LayerPermissionsFilter


class EovKeywordSerializer(serializers.ModelSerializer):
    class Meta:
        model = ThesaurusKeyword
        fields = ["id", "about", "alt_label"]


class MinimalLayerSerializer(DynamicModelSerializer):
    class Meta:
        model = Layer
        name = 'layer'
        view_name = 'layers-list'
        fields = (
            'pk', 'name', 'title'
        )

    name = serializers.CharField(read_only=True)


class EovKeywordViewSet(ListModelMixin, GenericViewSet):
    permission_classes = [AllowAny, ]
    queryset = ThesaurusKeyword.objects.all().filter(about__icontains="goosocean.org/eov")
    serializer_class = EovKeywordSerializer


class ReadinessKeywordViewSet(ListModelMixin, GenericViewSet):
    permission_classes = [AllowAny, ]
    queryset = ThesaurusKeyword.objects.all().filter(about__icontains="goosocean.org/readiness")
    serializer_class = EovKeywordSerializer


class ReadinessDataKeywordViewSet(ListModelMixin, GenericViewSet):
    permission_classes = [AllowAny, ]
    queryset = ThesaurusKeyword.objects.all().filter(about__icontains="goosocean.org/readiness/data")
    serializer_class = EovKeywordSerializer


class ReadinessRequirementsKeywordViewSet(ListModelMixin, GenericViewSet):
    permission_classes = [AllowAny, ]
    queryset = ThesaurusKeyword.objects.all().filter(about__icontains="goosocean.org/readiness/requirements")
    serializer_class = EovKeywordSerializer


class ReadinessCoordinationKeywordViewSet(ListModelMixin, GenericViewSet):
    permission_classes = [AllowAny, ]
    queryset = ThesaurusKeyword.objects.all().filter(about__icontains="goosocean.org/readiness/coordination")
    serializer_class = EovKeywordSerializer


class GoosFilterBackend(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):

        if request.query_params.get("eovs"):
            eov_ids = [eid for eid in request.query_params.get("eovs").split(",")]
            queryset = queryset.filter(tkeywords__in=eov_ids).distinct()

        if request.query_params.get("subvariables"):
            sv_ids = [svid for svid in request.query_params.get("subvariables").split(",")]
            queryset = queryset.filter(tkeywords__in=sv_ids).distinct()

        if request.query_params.get("readiness"):
            readiness_ids = [rid for rid in request.query_params.get("readiness").split(",")]
            queryset = queryset.filter(tkeywords__in=readiness_ids).distinct()

        return queryset


class MinimalLayerViewSet(DynamicModelViewSet):
    authentication_classes = [SessionAuthentication, BasicAuthentication, OAuth2Authentication]
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [
        DynamicFilterBackend, DynamicSortingFilter, DynamicSearchFilter,
        ExtentFilter, LayerPermissionsFilter, GoosFilterBackend
    ]
    queryset = Layer.objects.all()
    serializer_class = MinimalLayerSerializer
    pagination_class = GeoNodeApiPagination
