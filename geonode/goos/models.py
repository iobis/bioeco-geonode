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

DATA_IN_OBIS_CHOICES = [
    ("no", "No; none of the biological data collected by the network is included in OBIS"),
    ("some", "Yes; some of the biological data collected by the network is included in OBIS"),
    ("all", "Yes; all of the biological data collected by the network is included in OBIS")
]


class EovResource(models.Model):

    url = models.URLField(max_length=2000, null=True, blank=True)
    sops = ArrayField(models.URLField(), verbose_name='SOPs', null=True, blank=True, help_text='List of SOP URLs, comma separated.')
    outputs = ArrayField(models.URLField(), verbose_name='Outputs', null=True, blank=True, help_text='List of outputs (products, applications), comma separated URLs.')
    obis_pub_interest = models.BooleanField(null=True, blank=True, verbose_name='Interest in publishing to OBIS')
    funding = models.TextField(null=True, blank=True, verbose_name='Funding')
    funding_sector = ArrayField(models.CharField(choices=FUNDING_SECTOR_CHOICES, max_length=30), null=True, blank=True)
    data_in_obis = models.CharField(choices=DATA_IN_OBIS_CHOICES, null=True, blank=True, max_length=30)

    def get_funding_sector_display(self):
        funding_sector_dict = dict(FUNDING_SECTOR_CHOICES)
        if self.funding_sector is not None:
            return [funding_sector_dict[sector] for sector in self.funding_sector]
        else:
            return None

    class Meta:
        abstract = True
