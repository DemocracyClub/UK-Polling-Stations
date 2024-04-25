from addressbase.models import Address
from data_importers.management.commands import BaseHalaroseCsvImporter
from django.core.exceptions import ObjectDoesNotExist


class Command(BaseHalaroseCsvImporter):
    council_id = "SWA"
    addresses_name = "2024-05-02/2024-02-27T15:04:31.542588/Eros_SQL_Output008.csv"
    stations_name = "2024-05-02/2024-02-27T15:04:31.542588/Eros_SQL_Output008.csv"
    elections = ["2024-05-02"]
    csv_encoding = "windows-1252"

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "10091617114",  # 5 DUNVANT PARK HOUSES, DUNVANT, SWANSEA, SA2 7SH
            "10010037747",  # FIRST FLOOR FLAT ABOVE YATES 1-4 CAER STREET, CITY CENTRE, SWANSEA, SA1 3PP
            "10094784277",  # ROOM A 116 OLDWAY CENTRE 39 HIGH STREET, CITY CENTRE, SWANSEA, SA1 1LD
            "100100401496",  # 37A HIGH STREET, GORSEINON, SWANSEA, SA4 4BT
            "10011729995",  # ROSE COTTAGE UNCLASSIFIED SECTION-Y2117, OXWICH, SWANSEA, SA3 1LN
            "10010058515",  # THE LAUNDRY MIDDLETON HALL UNCLASSIFIED SECTION-Y2400, RHOSSILI, SWANSEA,SA3 1PJ
            "10010046963",  # LLE'R FEDWEN FARM, FELINDRE, SWANSEA
        ]:
            return None

        if record.housepostcode in [
            # split
            "SA6 6DS",
            "SA1 8PN",
            "SA1 6NQ",
            "SA5 7HY",
            "SA4 3QX",
            "SA3 3JS",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # Llangyfelach Church Hall Swansea Road Llangyfelach Swansea
        if (record.pollingstationnumber, record.pollingstationname) == (
            "7",
            "Llangyfelach Church Hall",
        ):
            record = record._replace(pollingstationpostcode="SA5 7JD")

        return super().station_record_to_dict(record)

    # quick fix to show maps for Halarose records that have a valid UPRN in the PollingVenueUPRN field
    def get_station_point(self, record):
        uprn = record.pollingvenueuprn.strip().lstrip("0")
        try:
            ab_rec = Address.objects.get(uprn=uprn)
            return ab_rec.location
        except ObjectDoesNotExist:
            return super().get_station_point(record)
