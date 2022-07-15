from geonode.api.urls import router
from django.urls import path

from . import views

router.register(r'eovs', views.EovKeywordViewSet, 'eovs')

router.register(r'readiness', views.ReadinessKeywordViewSet, 'readiness')
router.register(r'readiness_data', views.ReadinessDataKeywordViewSet, 'readiness_data')
router.register(r'readiness_requirements', views.ReadinessRequirementsKeywordViewSet, 'readiness_requirements')
router.register(r'readiness_coordination', views.ReadinessCoordinationKeywordViewSet, 'readiness_coordination')

router.register(r'layers_minimal', views.MinimalLayerViewSet, 'layers_minimal')
router.register(r'layer_statistics', views.LayerStatistics, 'layer_statistics')

urlpatterns = []
