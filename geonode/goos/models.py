from django.db import models
from geonode.goos.enumerations import READINESS_LEVELS


class Eov(models.Model):

    name = models.CharField(max_length=200)
    short_name = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField()
    url = models.URLField(max_length=200, null=True, blank=True)

    def __str__(self):
        return str(self.name)


class EovResource(models.Model):

    eovs = models.ManyToManyField(Eov, blank=True)

    readiness_requirements = models.CharField(
        max_length=100,
        choices=READINESS_LEVELS,
        blank=True,
        null=True
    )
    readiness_coordination = models.CharField(
        max_length=100,
        choices=READINESS_LEVELS,
        blank=True,
        null=True
    )
    readiness_data = models.CharField(
        max_length=100,
        choices=READINESS_LEVELS,
        blank=True,
        null=True
    )

    url = models.URLField(max_length=2000, null=True, blank=True)

    class Meta:
        abstract = True
