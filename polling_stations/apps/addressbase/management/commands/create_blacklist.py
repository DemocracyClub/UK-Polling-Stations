from django.db import connection
from django.conf import settings
from django.core.management.base import BaseCommand
from addressbase.models import Blacklist


"""
Use AddressBase and a lookup to ONS Local
Authority ids to create a list of postcodes
which contain UPRNs in >1 local authorities
"""


class Command(BaseCommand):
    def get_bad_postcodes(self):
        # get a list of postcodes containing UPRNs in >1 local authorities
        self.cursor.execute(
            """
            SELECT DISTINCT(postcode)
            FROM addressbase_address as AB
            JOIN addressbase_uprntocouncil UC
            ON AB.uprn = UC.uprn
            GROUP BY postcode
            HAVING COUNT(DISTINCT(LAD))>1;
            """
        )
        postcodes = self.cursor.fetchall()
        return [postcode[0] for postcode in postcodes]

    def get_councils(self, postcode):
        # get a list of local auths containing 1 or more UPRNs in postcode
        self.cursor.execute(
            """
            SELECT DISTINCT(LAD)
            FROM addressbase_address as AB
            JOIN addressbase_uprntocouncil UC
            ON AB.uprn = UC.uprn
            WHERE AB.postcode=%s;
            """,
            [postcode],
        )
        councils = self.cursor.fetchall()

        # merge/de-dupe any new councils not in uprn to council lookup
        gss_codes = [council[0] for council in councils]
        gss_codes = [
            settings.OLD_TO_NEW_MAP[code] if code in settings.OLD_TO_NEW_MAP else code
            for code in gss_codes
        ]
        gss_codes = list(set(gss_codes))
        if len(gss_codes) == 1:
            return []
        return gss_codes

    def handle(self, *args, **kwargs):
        self.cursor = connection.cursor()
        print("clearing existing data..")
        self.cursor.execute("TRUNCATE TABLE addressbase_blacklist;")

        print("blacklisting postcodes..")
        postcodes = self.get_bad_postcodes()

        for postcode in postcodes:
            councils = self.get_councils(postcode)
            for council in councils:
                Blacklist.objects.create(postcode=postcode, lad=council)

        self.cursor.execute(
            """
            UPDATE addressbase_blacklist
            SET postcode=REPLACE(postcode, ' ', '')
            """
        )

        print("...done")
