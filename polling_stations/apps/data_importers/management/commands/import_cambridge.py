from addressbase.models import UprnToCouncil
from core.opening_times import OpeningTimes
from data_importers.management.commands import BaseHalarose2026UpdateCsvImporter
from data_importers.mixins import AdvanceVotingMixin
from pollingstations.models import AdvanceVotingStation

from django.contrib.gis.geos import Point


class Command(BaseHalarose2026UpdateCsvImporter, AdvanceVotingMixin):
    council_id = "CAB"
    addresses_name = "2026-05-07/2026-02-16T14:26:03.938575/Democracy Club - Idox_2026-02-16 14-12.csv"
    stations_name = "2026-05-07/2026-02-16T14:26:03.938575/Democracy Club - Idox_2026-02-16 14-12.csv"
    elections = ["2026-05-07"]

    def station_record_to_dict(self, record):
        # Adding missing UPRN from council for:
        # The Church of Jesus Christ of Latter-day Saints 670 Cherry Hinton Road Cambridge CB1 8ED
        if self.get_station_hash(record) in [
            "18-the-church-of-jesus-christ-of-latter-day-saints",
            "17-the-church-of-jesus-christ-of-latter-day-saints",
        ]:
            record = record._replace(
                pollingvenueuprn="200004216747",
                pollingvenueeasting="548424",
                pollingvenuenorthing="256186",
            )

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        if record.uprn in [
            "10090966442",  # RIVERBOAT TUMBLING WATER G20635 RIVERSIDE, CAMBRIDGE
        ]:
            return None

        if record.postcode in [
            "CB3 0UW",  # split
        ]:
            return None
        return super().address_record_to_dict(record)

    def add_advance_voting_stations(self):
        # https://www.cambridge.gov.uk/early-voting-trial

        opening_times = OpeningTimes()
        # Thursday 30 April, from 9am to 6pm
        opening_times.add_open_time("2026-04-30", "09:00", "18:00")
        # Friday 1 May, from 9am to 6pm
        opening_times.add_open_time("2026-05-01", "09:00", "18:00")
        # Saturday 2 May, from 9am to 6pm
        opening_times.add_open_time("2026-05-02", "09:00", "18:00")

        # Clay Farm Centre, Hobson Square, Trumpington, Cambridge CB2 9FN
        clay_farm_avs = AdvanceVotingStation(
            name="Clay Farm Centre",
            address="""Hobson Square,
            Trumpington,
            Cambridge
            """,
            postcode="CB2 9FN",
            location=Point(0.1200693, 52.1735637, srid=4326),
            opening_times=opening_times.as_string_table(),
            council=self.council,
        )
        clay_farm_avs.save()

        # The Guildhall, Market Square, Cambridge CB2 3QJ – use the entrance on Peas Hill, via the tourist information centre
        guildhall_avs = AdvanceVotingStation(
            name="The Guildhall",
            address="""Market Square,
            Cambridge,
            (Use the entrance on Peas Hill, via the tourist information centre.)
            """,
            postcode="CB2 3QJ",
            location=Point(0.1194016, 52.2044499, srid=4326),
            opening_times=opening_times.as_string_table(),
            council=self.council,
        )
        guildhall_avs.save()

        # Meadows Community Centre, 299, Arbury Road, Cambridge CB4 2JL
        meadows_community_centre_avs = AdvanceVotingStation(
            name="Meadows Community Centre",
            address="""299 Arbury Road,
            Cambridge
            """,
            postcode="CB4 2JL",
            location=Point(0.1194436, 52.2307243, srid=4326),
            opening_times=opening_times.as_string_table(),
            council=self.council,
        )
        meadows_community_centre_avs.save()

        # Assign all UPRNs to all alternative stations
        for station in (clay_farm_avs, guildhall_avs, meadows_community_centre_avs):
            uprn_ids = UprnToCouncil.objects.filter(
                lad=self.council.geography.gss
            ).values_list("uprn", flat=True)

            self.assign_advance_voting_stations(station, uprn_ids)
