from django.contrib.gis.db import models

from django_extensions.db.models import TimeStampedModel

from councils.models import Council


class LoggedPostcode(TimeStampedModel):
    postcode = models.CharField(max_length=100)
    had_data = models.BooleanField(default=False, db_index=True)
    location = models.PointField(null=True, blank=True)
    council = models.ForeignKey(Council, null=True, db_index=True)
    brand = models.CharField(blank=True, max_length=100, db_index=True)
    utm_source = models.CharField(blank=True, max_length=100, db_index=True)
    utm_medium = models.CharField(blank=True, max_length=100, db_index=True)
    utm_campaign = models.CharField(blank=True, max_length=100, db_index=True)
    language = models.CharField(blank=True, max_length=5)
    view_used = models.CharField(blank=True, max_length=100)


    def __str__(self):
        return "{0} ({1})".format(
            self.postcode,
            self.brand,
        )

class CampaignSignup(TimeStampedModel):
    postcode = models.CharField(max_length=100, blank=False)
    name = models.CharField(max_length=100, blank=False)
    email = models.EmailField(blank=False)
    join_list = models.BooleanField(default=False)
