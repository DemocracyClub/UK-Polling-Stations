from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter
from django.contrib.gis.geos import Point


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "WLV"
    addresses_name = (
        "2023-05-04/2023-02-28T09:51:32.288722/Democracy_Club__04May2023.tsv"
    )
    stations_name = (
        "2023-05-04/2023-02-28T09:51:32.288722/Democracy_Club__04May2023.tsv"
    )
    elections = ["2023-05-04"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10093325431",  # 2A RAYNOR ROAD, WOLVERHAMPTON
            "10090643975",  # 11 KIRKWALL CRESCENT, WOLVERHAMPTON
            "10093326250",  # FLAT 1, SMART BUILDING, VULCAN ROAD, BILSTON
            "10007124221",  # MOSELEY COURT LODGE, BRIDAL WAY, NORTHYCOTE LANE, WOLVERHAMPTON
            "10090641653",  # 1 HENRY FOWLER DRIVE, WOLVERHAMPTON
            "10090641654",  # 3 HENRY FOWLER DRIVE, WOLVERHAMPTON
            "10090641655",  # 4 HENRY FOWLER DRIVE, WOLVERHAMPTON
            "10090641656",  # 5 HENRY FOWLER DRIVE, WOLVERHAMPTON
            "10090641657",  # 6 HENRY FOWLER DRIVE, WOLVERHAMPTON
            "100071556719",  # THE CHIP INN, 32 THORNEYCROFT LANE, WOLVERHAMPTON
        ]:
            return None

        if record.addressline6 in ["WV13 3RG"]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        rec = super().station_record_to_dict(record)

        # [WRONG LOC] St Joseph`s Church Hall, Coalway Road,  Wolverhampton
        if rec["internal_council_id"] == "30057":
            rec["location"] = Point(-2.170664443278646, 52.57076293329278, srid=4326)

        # [WRONG LOC] Moathouse Community Centre, 52 Moathouse Lane East, Wednesfield
        if rec["internal_council_id"] == "30219":
            rec["location"] = Point(-2.0731047162921405, 52.608227577664984, srid=4326)

        return rec
