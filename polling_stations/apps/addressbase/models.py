from django.contrib.gis.db import models


class AddressManager(models.GeoManager):
    def postcodes_for_district(self, district):
        qs = self.filter(location__within=district.area)
        qs = qs.values_list('postcode', flat=True).distinct()
        return list(qs)

    def points_for_postcode(self, postcode):
        qs = self.filter(postcode=postcode)
        qs = qs.values_list('location', flat=True)
        return list(qs)


class AbstractAddress(models.Model):
    uprn = models.CharField(primary_key=True, max_length=100)
    address = models.TextField(blank=True)
    postcode = models.CharField(blank=True, max_length=15, db_index=True)
    location = models.PointField(null=True, blank=True)

    class Meta:
        abstract = True


class Address(AbstractAddress):
    objects = AddressManager()


class AbstractOnsud(models.Model):
    uprn = models.CharField(primary_key=True, max_length=12)
    """
    Note: this is not a FK to Address because the ONSUD is released quarterly
    and AddressBase is released every 6 weeks, so these 2 sources won't
    necessarily match up exactly.

    Like every aspect of this project, it is *not that simple*
    """
    ctry_flag = models.CharField(blank=True, max_length=1)
    cty = models.CharField(blank=True, max_length=9)
    lad = models.CharField(blank=True, max_length=9)
    ward = models.CharField(blank=True, max_length=9)
    hlthau = models.CharField(blank=True, max_length=9)
    ctry = models.CharField(blank=True, max_length=9)
    rgn = models.CharField(blank=True, max_length=9)
    pcon = models.CharField(blank=True, max_length=9)
    eer = models.CharField(blank=True, max_length=9)
    ttwa = models.CharField(blank=True, max_length=9)
    nuts = models.CharField(blank=True, max_length=9)
    park = models.CharField(blank=True, max_length=9)
    oa11 = models.CharField(blank=True, max_length=9)
    lsoa11 = models.CharField(blank=True, max_length=9)
    msoa11 = models.CharField(blank=True, max_length=9)
    parish = models.CharField(blank=True, max_length=9)
    wz11 = models.CharField(blank=True, max_length=9)
    ccg = models.CharField(blank=True, max_length=9)
    bua11 = models.CharField(blank=True, max_length=9)
    buasd11 = models.CharField(blank=True, max_length=9)
    ruc11 = models.CharField(blank=True, max_length=2)
    oac11 = models.CharField(blank=True, max_length=3)
    lep1 = models.CharField(blank=True, max_length=9)
    lep2 = models.CharField(blank=True, max_length=9)
    pfa = models.CharField(blank=True, max_length=9)
    imd = models.CharField(blank=True, max_length=5)

    class Meta:
        abstract = True


class Onsud(AbstractOnsud):
    pass


class Blacklist(models.Model):
    """
    Model for storing postcodes containing UPRNs in >1 local authorities
    This is intentionally de-normalised for performance reasons
    Ideally ('postcode', 'lad') should be a composite PK,
    but django's ORM doesn't support them.
    """
    postcode = models.CharField(blank=False, max_length=15, db_index=True)
    lad = models.CharField(blank=False, max_length=9)

    class Meta:
        unique_together = (('postcode', 'lad'))
