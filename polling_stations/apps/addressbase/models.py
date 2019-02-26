from django.contrib.gis.db import models
from django.db import connection
from uk_geo_utils.models import AbstractAddress, AbstractAddressManager, AbstractOnsud


class AddressManager(AbstractAddressManager):
    def postcodes_for_district(self, district):
        qs = self.filter(location__within=district.area)
        qs = qs.values_list("postcode", flat=True).distinct()
        return list(qs)

    def points_for_postcode(self, postcode):
        qs = self.filter(postcode=postcode)
        qs = qs.values_list("location", flat=True)
        return list(qs)


class Address(AbstractAddress):
    objects = AddressManager()


class Onsud(AbstractOnsud):
    class Meta:
        index_together = ("lad",)


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
        unique_together = ("postcode", "lad")


def get_uprn_hash_table(council_id):
    # get all the UPRNs in target local auth
    # which exist in both Addressbase and ONSUD
    cursor = connection.cursor()
    cursor.execute(
        """
        SELECT
            a.uprn,
            a.address,
            REPLACE(a.postcode, ' ', ''),
            a.location
        FROM addressbase_address a
        JOIN addressbase_onsud o ON a.uprn=o.uprn
        WHERE o.lad=%s;
        """,
        [council_id],
    )
    # return result a hash table keyed by UPRN
    return {
        row[0]: {"address": row[1], "postcode": row[2], "location": row[3]}
        for row in cursor.fetchall()
    }
