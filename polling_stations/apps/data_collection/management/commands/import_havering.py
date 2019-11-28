from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E09000016"
    addresses_name = "parl.2019-12-12/Version 1/Democracy_Club__12December2019haver.tsv"
    stations_name = "parl.2019-12-12/Version 1/Democracy_Club__12December2019haver.tsv"
    elections = ["parl.2019-12-12"]
    csv_delimiter = "\t"
    allow_station_point_from_postcode = False

    def station_record_to_dict(self, record):

        # File supplied contained obviously inaccurate point
        # Replace with correction from council
        # The Mawney Foundation School
        if record.polling_place_id == "8241":
            record = record._replace(polling_place_easting="550712.13")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10091581050",
        ]:
            return None

        return rec
