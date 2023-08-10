from councils.models import Council
from django.db import models


class DataQuality(models.Model):
    class Meta:
        verbose_name_plural = "Data Quality"

    def __unicode__(self):
        return "Data quality for %s" % self.council

    council = models.OneToOneField(
        Council,
        primary_key=True,
        on_delete=models.CASCADE,
    )
    report = models.TextField(blank=True)
    num_stations = models.IntegerField(default=0)
    num_districts = models.IntegerField(default=0)
    num_addresses = models.IntegerField(default=0)


from django.db.models.signals import post_save


def council_saved(sender, **kwargs):
    DataQuality.objects.get_or_create(council=kwargs["instance"])


post_save.connect(council_saved, sender=Council)
