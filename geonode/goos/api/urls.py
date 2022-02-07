from geonode.api.urls import router

from . import views

router.register(r'eovs', views.EovKeywordViewSet, 'eovs')

router.register(r'readiness_data', views.ReadinessDataKeywordViewSet, 'readiness_data')
router.register(r'readiness_requirements', views.ReadinessRequirementsKeywordViewSet, 'readiness_requirements')
router.register(r'readiness_coordination', views.ReadinessCoordinationKeywordViewSet, 'readiness_coordination')

router.register(r'layers_minimal', views.MinimalLayerViewSet, 'layers_minimal')

urlpatterns = []
