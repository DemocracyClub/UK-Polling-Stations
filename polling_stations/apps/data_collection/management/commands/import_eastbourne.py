from data_collection.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "E07000061"
    addresses_name = (
        "parl.2019-12-12/Version 1/polling_station_export-2019-11-07east.csv"
    )
    stations_name = (
        "parl.2019-12-12/Version 1/polling_station_export-2019-11-07east.csv"
    )
    elections = ["parl.2019-12-12"]
    allow_station_point_from_postcode = False

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "10093961546",
            "10010653214",
            "10010654823",
        ]:
            return None

        if uprn in [
            "10010663461",  # BN211HG -> BN211HH : THE LAMBE INN HIGH STREET, EASTBOURNE, EAST SUSSEX
        ]:
            rec["accept_suggestion"] = True

        if uprn in [
            "10024140467",  # BN213EU -> BN228AG : 143 / 145 LANGNEY ROAD, EASTBOURNE, EAST SUSSEX
            "100061919876",  # BN208NH -> BN208NR : THE DRIVE 153 VICTORIA DRIVE, EASTBOURNE, EAST SUSSEX
        ]:
            rec["accept_suggestion"] = False

        return rec
