from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.db import models

from councils.models import Council


class DataQuality(models.Model):
    council = models.OneToOneField(Council)
    url = models.URLField(blank=True, verbose_name="URL to the data",
        help_text="(PDF, website, etc)")
    data_format = models.CharField(blank=True, max_length=100,
        help_text="PDF, CSV, etc")
    has_polling_stations_online = models.BooleanField(default=False)
    has_polling_discricts_online = models.BooleanField(default=False)
    needs_manually_importing = models.BooleanField(default=False,
        help_text="i.e. copying and pasting from a PDF")
    public_notes = models.TextField(blank=True)
    in_contact_with_dc = models.BooleanField(default=False,
        verbose_name="In contact with DC?",
        help_text="Have we heard from them directly?")

    class Meta:
        verbose_name_plural = "Data Quality"

    def __unicode__(self):
        return "Data quality for %s" % self.council