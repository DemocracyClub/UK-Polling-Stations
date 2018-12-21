import logging
from collections import namedtuple
from django.db import connection
from councils.models import Council
from pollingstations.models import PollingDistrict, ResidentialAddress
from uk_geo_utils.helpers import Postcode
from addressbase.models import Address


AddressTuple = namedtuple(
    "Address",
    [
        "address",
        "postcode",
        "council_id",
        "polling_station_id",
        "slug",
        "uprn",
        "location",
    ],
)


class AddressSet(set):
    def save(self, batch_size):

        addresses_db = []
        for address in self:
            record = ResidentialAddress(
                address=address.address,
                postcode=Postcode(address.postcode).without_space,
                polling_station_id=address.polling_station_id,
                council_id=address.council_id,
                slug=address.slug,
                uprn=address.uprn,
                location=address.location,
            )
            addresses_db.append(record)

        ResidentialAddress.objects.bulk_create(addresses_db, batch_size=batch_size)


class EdgeCaseFixer:
    def __init__(self, target_council_id, logger):
        self.address_set = AddressSet()
        self.target_council_id = target_council_id
        self.logger = logger
        self.AddressRecord = namedtuple(
            "AddressRecord",
            [
                "uprn",
                "address",
                "postcode",
                "district_id",
                "station_id",
                "council_id",
                "count",
                "location",
            ],
        )

    def unpack_address(self, record):
        return self.AddressRecord(*record)

    def get_station_id(self, address):
        if not address.council_id:
            c = Council.objects.defer("area").get(area__covers=address.location)
            council_id = c.council_id
        else:
            council_id = address.council_id

        if council_id != self.target_council_id:
            # treat addresses in other council areas as district not found
            raise PollingDistrict.DoesNotExist

        if address.count > 1:
            raise PollingDistrict.MultipleObjectsReturned

        if not address.district_id:
            raise PollingDistrict.DoesNotExist

        if address.station_id:
            polling_station = address.station_id
        else:
            """
            We do not know which station this district is served by (orphan district)

            Because we have no way of knowing what the correct station is, intentionally insert a record with an empty station id
            This allows us to *list* the address, but if the user *chooses* it, we will show "we don't know: call your council"
            """
            polling_station = ""

        return polling_station

    def make_addresses_for_postcode(self, postcode):
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT
                ab.uprn,
                ab.address,
                ab.postcode,
                pd.internal_council_id,
                ps.internal_council_id,
                os.lad,
                ct.count,
                ab.location
            FROM addressbase_address ab

            LEFT JOIN pollingstations_pollingdistrict pd
            ON ST_CONTAINS(pd.area, ab.location)

            LEFT JOIN addressbase_onsud os
            ON os.uprn=ab.uprn

            LEFT JOIN pollingstations_pollingstation ps
            ON (
                (pd.polling_station_id=ps.internal_council_id
                    AND pd.council_id=ps.council_id)
                OR
                (pd.internal_council_id=ps.polling_district_id
                    AND pd.council_id=ps.council_id)
            )

            JOIN (
                SELECT
                    ab.uprn,
                    COUNT(*) AS count
                FROM addressbase_address ab
                LEFT JOIN pollingstations_pollingdistrict pd
                ON ST_CONTAINS(pd.area, ab.location)
                WHERE ab.postcode=%s
                GROUP BY ab.uprn
            ) ct
            ON ab.uprn=ct.uprn

            WHERE ab.postcode=%s
            """,
            [postcode, postcode],
        )
        addresses = cursor.fetchall()

        for record in addresses:
            address = self.unpack_address(record)
            try:
                station_id = self.get_station_id(address)
            except PollingDistrict.DoesNotExist:
                # Chances are this is on the edge of the council area, and
                # we don't have data for the area the property is in
                # TODO: handle this
                continue
            except PollingDistrict.MultipleObjectsReturned:
                """
                This is normally caused by districts that overlap

                Because we have no way of knowing what the correct station is, intentionally insert a record with an empty station id
                This allows us to *list* the address, but if the user *chooses* it, we will show "we don't know: call your council"
                """

                self.logger.log_message(
                    logging.WARNING,
                    "Found address contained by >1 polling districts - data may contain overlapping polygons:\n%s\n%s\n",
                    variable=(address.address, address.postcode),
                )

                station_id = ""
            except Council.DoesNotExist:
                self.logger.log_message(
                    logging.WARNING,
                    "Skipping address which could not be assigned to a local authority:\n%s\n%s\n",
                    variable=(address.address, address.postcode),
                )
                continue

            self.address_set.add(
                AddressTuple(
                    address.address,
                    postcode,
                    self.target_council_id,
                    station_id,
                    address.uprn,
                    address.uprn,
                    address.location,
                )
            )

    def get_address_set(self):
        return self.address_set


def district_contains_all_points(district, points):
    return all([district.area.contains(p) for p in points])


def postcodes_not_contained_by_district(district):
    data = {"not_contained": [], "total": 0}

    for postcode in Address.objects.postcodes_for_district(district):
        points = Address.objects.points_for_postcode(postcode)
        data["total"] += 1
        if not district_contains_all_points(district, points):
            data["not_contained"].append(postcode)
    return data


def create_address_records_for_council(council, batch_size, logger):
    postcode_report = {
        "no_attention_needed": 0,
        "addresses_created": 0,
        "postcodes_needing_address_lookup": set(),
    }

    fixer = EdgeCaseFixer(council.pk, logger)
    for district in PollingDistrict.objects.filter(council=council):
        data = postcodes_not_contained_by_district(district)

        postcode_report["no_attention_needed"] += data["total"] - len(
            data["not_contained"]
        )
        postcode_report["postcodes_needing_address_lookup"].update(
            data["not_contained"]
        )

        for postcode in data["not_contained"]:
            fixer.make_addresses_for_postcode(postcode)

    address_set = fixer.get_address_set()
    address_set.save(batch_size)
    postcode_report["addresses_created"] = len(address_set)

    return postcode_report
