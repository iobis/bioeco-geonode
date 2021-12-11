from django.db import models


class EovResource(models.Model):

    url = models.URLField(max_length=2000, null=True, blank=True)

    class Meta:
        abstract = True
