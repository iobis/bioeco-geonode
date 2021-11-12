from django.conf.urls import url, include

urlpatterns = [
    url(r'^', include('geonode.goos.api.urls'))
]
