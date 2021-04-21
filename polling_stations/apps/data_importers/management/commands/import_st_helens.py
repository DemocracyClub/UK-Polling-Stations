from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "SHN"
    addresses_name = "2021-04-06T14:46:11.580651/Democracy_Club__06May2021.tsv"
    stations_name = "2021-04-06T14:46:11.580651/Democracy_Club__06May2021.tsv"
    elections = ["2021-05-06"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):
        # Sutton Village Church, Herbert Street
        if record.polling_place_id == "4264":
            record = record._replace(polling_place_easting="0")
            record = record._replace(polling_place_northing="0")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):

        uprn = record.property_urn.strip().lstrip("0")
        if uprn in ["39081348"]:
            return None
        if record.addressline6 in [
            "WA9 4QJ",
            "WA11 0LA",
            "WA11 9TB",
            "WA9 3RR",
            "WA9 3UF",
            "WA10 1JT",
            "WA9 3ZL",
        ]:
            return None
        return super().address_record_to_dict(record)
