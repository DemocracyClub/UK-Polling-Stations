from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000096"
    addresses_name = (
        "parl.2019-12-12/Version 2/Democracy_Club__12December2019dacorum.CSV"
    )
    stations_name = (
        "parl.2019-12-12/Version 2/Democracy_Club__12December2019dacorum.CSV"
    )
    elections = ["parl.2019-12-12"]
    csv_delimiter = ","
    allow_station_point_from_postcode = False

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)

        if record.addressline6 in [
            "AL3 8LR",
            "HP4 2RS",
        ]:
            return None

        return rec
