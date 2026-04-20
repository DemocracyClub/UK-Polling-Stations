from django.contrib.gis.geos import Point

from addressbase.models import UprnToCouncil
from core.opening_times import OpeningTimes
from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter
from data_importers.mixins import AdvanceVotingMixin
from pollingstations.models import AdvanceVotingStation


# This comment communicates no useful information
# I just had to change the file to force it to run


class Command(BaseXpressDemocracyClubCsvImporter, AdvanceVotingMixin):
    council_id = "TUN"
    addresses_name = (
        "2026-05-07/2026-02-10T13:29:01.152535/Democracy_Club__07May2026 - 10Feb.tsv"
    )
    stations_name = (
        "2026-05-07/2026-02-10T13:29:01.152535/Democracy_Club__07May2026 - 10Feb.tsv"
    )
    elections = ["2026-05-07"]
    csv_encoding = "windows-1252"
    csv_delimiter = "\t"

    # Ignore warnings about addressbase postcode for below stations - council decision:
    # - St Barnabas Hall, Quarry Road, Tunbridge Wells
    # - The Hub, Grosvenor Recreation Ground, Auckland Road, Royal Tunbridge Wells
    # - St James Church Hall, St James Road, Royal Tunbridge Wells
    # - St Mark`s Hall, Bayham Road, Royal Tunbridge Wells
    # - The Library, Number One Community Centre, Rowan Tree Road, Tunbridge Wells

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "100062544084",  # COURTYARD FLAT, COLEBROOKE, PEMBURY ROAD, TONBRIDGE
            "100062543933",  # COLEBROOKE HOUSE, PEMBURY ROAD, TONBRIDGE
            "100061193913",  # HUNTERS LODGE, PEMBURY ROAD, TONBRIDGE
            "100062551952",  # BLACK BUSH COTTAGE, BEDGEBURY ROAD, GOUDHURST, Cranbrook
            "10090055018",  # CRABTREE HOUSE, COURSE HORN LANE, CRANBROOK
            "10008666136",  # NIGHTINGALE COTTAGE, CONGHURST LANE, HAWKHURST, CRANBROOK
            "100062543979",  # 1 BROOK FARM COTTAGES, FIVE OAK GREEN ROAD, TONBRIDGE
        ]:
            return None

        if record.addressline6 in [
            # split
            "TN3 0HX",
            "TN4 0AB",
            # suspect
            "TN12 7BZ",
        ]:
            return None

        return super().address_record_to_dict(record)

    def add_advance_voting_stations(self):
        # https://tunbridgewells.gov.uk/council/voting-and-elections/elections/voter-hubs

        opening_times = OpeningTimes()

        # Saturday 2 May, from 9am to 6pm
        opening_times.add_open_time("2026-05-02", "09:00", "18:00")
        # Sunday 3 May, from 10.30am to 4.30pm
        opening_times.add_open_time("2026-05-03", "10:30", "16:30")

        # Royal Victoria Place, Royal Tunbridge Wells, TN1 2SS - Pop in Pop up unit, upper mall near M&S
        royal_victoria_place_avs = AdvanceVotingStation(
            name="Royal Victoria Place",
            address="""Pop in Pop up unit, upper mall near M&S,
            Royal Tunbridge Wells,
            """,
            postcode="TN1 2SS",
            location=Point(0.2657803, 51.1344536, srid=4326),
            opening_times=opening_times.as_string_table(),
            council=self.council,
        )
        royal_victoria_place_avs.save()

        # Paddock Wood Community Centre, Maidstone Road, Paddock Wood, TN12 6EB
        paddock_wood_avs = AdvanceVotingStation(
            name="Paddock Wood Community Centre",
            address="""Maidstone Road,
            Paddock Wood,
            """,
            postcode="TN12 6EB",
            location=Point(0.3831702, 51.1748044, srid=4326),
            opening_times=opening_times.as_string_table(),
            council=self.council,
        )
        paddock_wood_avs.save()

        # Vestry Hall, Stone Street, Cranbrook, TN17 3HA
        vestry_hall_avs = AdvanceVotingStation(
            name="Vestry Hall",
            address="""Stone Street,
            Cranbrook
            """,
            postcode="TN17 3HA",
            location=Point(0.5356726, 51.0966124, srid=4326),
            opening_times=opening_times.as_string_table(),
            council=self.council,
        )
        vestry_hall_avs.save()

        # Assign all UPRNs to all alternative stations
        for station in (royal_victoria_place_avs, paddock_wood_avs, vestry_hall_avs):
            uprn_ids = UprnToCouncil.objects.filter(
                lad=self.council.geography.gss
            ).values_list("uprn", flat=True)

            self.assign_advance_voting_stations(station, uprn_ids)
