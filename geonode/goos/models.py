from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.utils.translation import ugettext_lazy as _


class EovResource(models.Model):

    url = models.URLField(max_length=2000, null=True, blank=True)
    sops = ArrayField(models.URLField(), verbose_name='SOPs', null=True, blank=True, help_text='List of SOP URLs, comma separated.')

    class Meta:
        abstract = True
