from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter

# from django.contrib.gis.geos import Point


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E09000020"
    addresses_name = "2020-03-03T13:22:45.003848/Democracy_Club__07May2020.tsv"
    stations_name = "2020-03-03T13:22:45.003848/Democracy_Club__07May2020.tsv"
    elections = ["2020-05-07"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in ["217125754", "217129279", "217130227", "217029293"]:
            return None

        if record.addressline6 == "SW3 3AA":
            return None
        if uprn == "217108045":
            rec["postcode"] = "W8 5DH"

        if (
            record.addressline6 == "W11 4LY"
            and record.addressline1 == "2B Drayson Mews"
        ):
            rec["postcode"] = "W8 4LY"

        return rec
