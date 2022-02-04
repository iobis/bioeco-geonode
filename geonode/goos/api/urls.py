from geonode.api.urls import router

from . import views

router.register(r'eovs', views.EovKeywordViewSet, 'eovs')

urlpatterns = []