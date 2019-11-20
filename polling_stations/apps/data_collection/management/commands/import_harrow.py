from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E09000015"
    addresses_name = (
        "parl.2019-12-12/Version 1/Democracy_Club__12December2019harrow.tsv"
    )
    stations_name = "parl.2019-12-12/Version 1/Democracy_Club__12December2019harrow.tsv"
    elections = ["parl.2019-12-12"]
    csv_delimiter = "\t"
    allow_station_point_from_postcode = False

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")
        rec = super().address_record_to_dict(record)

        if uprn in ["100021313639", "100021287919", "100021254576"]:
            return None

        if uprn == "10091092216":
            rec["postcode"] = "HA2 0LH"

        return rec
