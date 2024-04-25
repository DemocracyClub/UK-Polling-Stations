from addressbase.models import Address
from data_importers.management.commands import BaseHalaroseCsvImporter
from django.core.exceptions import ObjectDoesNotExist


class Command(BaseHalaroseCsvImporter):
    council_id = "MEN"
    addresses_name = "2024-05-02/2024-02-27T10:25:12.441978/Eros_SQL_Output001 (2).csv"
    stations_name = "2024-05-02/2024-02-27T10:25:12.441978/Eros_SQL_Output001 (2).csv"
    elections = ["2024-05-02"]

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "250056648",  # WILLS FARM, PRIDDY, WELLS
            "250045108",  # ORCHARD BYRE, POLSHAM, WELLS
            "250070118",  # NEW MANOR FARM, POLSHAM, WELLS
            "250003895",  # TWIN OAKS, SOMERTON ROAD, STREET
            "250003837",  # LEIGHOLT FARM, SOMERTON ROAD, STREET
            "250081238",  # FLAT 1, 13 PRINTWORKS ROAD, FROME
            "250081239",  # FLAT 2, 13 PRINTWORKS ROAD, FROME
            "250070558",  # THE BELL TOWER ORCHARDLEIGH VILLAGE PUMP TO LULLINGTON LANE, LULLINGTON, FROME
            "250070559",  # THE CLOCK TOWER ORCHARDLEIGH VILLAGE PUMP TO LULLINGTON LANE, LULLINGTON, FROME
            "250046922",  # HEARTY GATE BUNGALOW, NORTH WOOTTON, SHEPTON MALLET
        ]:
            return None

        if record.housepostcode in [
            # split
            "BA16 0NU",
            "BA4 4DP",
            "BA11 2ED",
            "BA11 5BT",
            "BA11 4SA",
            "BA11 2TQ",
            "BA11 2XG",
            "BA11 1NB",
            "BA16 0BD",
            "BA11 4AJ",
            "BA5 1RJ",
            "BA11 5HA",
            "BA6 9DH",
            "BA11 2AU",
            "BA11 5DU",
            "BA4 6SY",
            "BA3 5QE",
            "BA3 4DN",
            "BA11 5EP",
            "BA11 4NY",
            "BA4 5HB",
            # suspect
            "BA11 5FE",  # MARIGOLD ROAD
            "BA11 1GN",  # PRINTWORKS ROAD
        ]:
            return None

        return super().address_record_to_dict(record)

    # quick fix to show maps for Halarose records that have a valid UPRN in the PollingVenueUPRN field
    def get_station_point(self, record):
        uprn = record.pollingvenueuprn.strip().lstrip("0")
        try:
            ab_rec = Address.objects.get(uprn=uprn)
            return ab_rec.location
        except ObjectDoesNotExist:
            return super().get_station_point(record)
