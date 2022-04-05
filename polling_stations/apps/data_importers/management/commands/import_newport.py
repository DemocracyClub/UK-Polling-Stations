from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "NWP"
    addresses_name = (
        "2022-05-05/2022-04-05T12:34:16.135232/Democracy_Club__05May2022.tsv"
    )
    stations_name = (
        "2022-05-05/2022-04-05T12:34:16.135232/Democracy_Club__05May2022.tsv"
    )
    elections = ["2022-05-05"]
    csv_encoding = "windows-1252"
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in ["10094537748"]:
            return None

        if record.post_code in [
            "NP19 9BX",
            "NP10 8NT",
            "NP10 8AT",
            "NP26 3AD",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):

        # East Hub 282 Ringland Circle Newport
        if record.polling_place_id == "12591":
            record = record._replace(polling_place_postcode="NP19 9PS")

        return super().station_record_to_dict(record)
