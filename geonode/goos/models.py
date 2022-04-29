from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.utils.translation import ugettext_lazy as _


FUNDING_SECTOR_CHOICES = [
    ("academia", "Academia"),
    ("civil_society", "Civil society"),
    ("industry", "Industry"),
    ("governmental", "Governmental"),
    ("other", "Other")
]


class EovResource(models.Model):

    url = models.URLField(max_length=2000, null=True, blank=True)
    sops = ArrayField(models.URLField(), verbose_name='SOPs', null=True, blank=True, help_text='List of SOP URLs, comma separated.')
    outputs = ArrayField(models.URLField(), verbose_name='Outputs', null=True, blank=True, help_text='List of outputs (products, applications), comma separated URLs.')
    obis_pub_interest = models.BooleanField(null=True, blank=True, verbose_name='Interest in publishing to OBIS')
    in_obis = models.BooleanField(null=True, blank=True, verbose_name='In OBIS')
    funding = models.TextField(null=True, blank=True, verbose_name='Funding')
    funding_sector = ArrayField(models.CharField(choices=FUNDING_SECTOR_CHOICES, max_length=30), null=True, blank=True)

    def get_funding_sector_display(self):
        funding_sector_dict = dict(FUNDING_SECTOR_CHOICES)
        return [funding_sector_dict[sector] for sector in self.funding_sector]

    class Meta:
        abstract = True
