from geonode.api.urls import router

from . import views

router.register(r'eovs', views.EovKeywordViewSet, 'eovs')
router.register(r'layers_minimal', views.MinimalLayerViewSet, 'layers_minimal')

urlpatterns = []
