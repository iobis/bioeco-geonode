from geonode.api.urls import router

from . import views

router.register(r'eovs', views.FastThesaurusKeywordViewSet, 'eovs')

urlpatterns = []