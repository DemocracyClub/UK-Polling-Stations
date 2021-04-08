from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "NKE"
    addresses_name = (
        "2021-03-23T12:06:26.706618/North Kesteven Democracy_Club__06May2021_1.tsv"
    )
    stations_name = (
        "2021-03-23T12:06:26.706618/North Kesteven Democracy_Club__06May2021_1.tsv"
    )
    elections = ["2021-05-06"]
    csv_delimiter = "\t"
    csv_encoding = "windows-1252"

    def station_record_to_dict(self, record):
        # Norton Disney Village Hall Main Street Norton Disney Lincoln LN6 9JU
        if record.polling_place_id == "6586":
            record = record._replace(polling_place_easting="")
            record = record._replace(polling_place_northing="")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10006545220",  # THE CROFT, ROXHOLM, SLEAFORD
        ]:
            return None

        if record.addressline6 in [
            "LN5 0JQ",
            "LN6 9EW",
            "LN6 9HW",
            "NG34 0BU",
            "LN4 1DJ",
            "NG34 0BQ",
            "LN4 1EP",
            "LN6 9PU",
            "LN4 2AB",
        ]:
            return None

        return super().address_record_to_dict(record)
