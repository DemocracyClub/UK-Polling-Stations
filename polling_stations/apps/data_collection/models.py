from django.db import models

from councils.models import Council


class DataQuality(models.Model):
    council = models.OneToOneField(Council, primary_key=True)
    url = models.URLField(
        blank=True, verbose_name="URL to the data", help_text="(PDF, website, etc)"
    )
    data_format = models.CharField(
        blank=True, max_length=100, help_text="PDF, CSV, etc"
    )
    has_polling_stations_online = models.BooleanField(default=False)
    has_polling_discricts_online = models.BooleanField(default=False)
    needs_manually_importing = models.BooleanField(
        default=False, help_text="i.e. copying and pasting from a PDF"
    )
    public_notes = models.TextField(blank=True)
    in_contact_with_dc = models.BooleanField(
        default=False,
        verbose_name="In contact with DC?",
        help_text="Have we heard from them directly?",
    )
    rating = models.DecimalField(
        blank=True, null=True, max_digits=1, help_text="From 0 to 9", decimal_places=0
    )
    report = models.TextField(blank=True)
    num_stations = models.IntegerField(default=0)
    num_districts = models.IntegerField(default=0)
    num_addresses = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = "Data Quality"
        ordering = ("rating",)

    def __unicode__(self):
        return "Data quality for %s" % self.council


from django.db.models.signals import post_save


def council_saved(sender, **kwargs):
    DataQuality.objects.get_or_create(council=kwargs["instance"])


post_save.connect(council_saved, sender=Council)
