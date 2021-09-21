from django.db import models


class Eov(models.Model):

    name = models.CharField(max_length=200)
    description = models.TextField()
    url = models.URLField(max_length=200, null=True, blank=True)

    def __str__(self):
        return str(self.name)
