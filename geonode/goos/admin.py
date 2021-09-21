from django.contrib import admin
from geonode.goos.models import Eov


class EovAdmin(admin.ModelAdmin):
    fields = ['name', 'description', 'url']


admin.site.register(Eov, EovAdmin)
