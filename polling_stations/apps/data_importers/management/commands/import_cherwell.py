from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "CHR"
    addresses_name = (
        "2022-05-05/2022-03-29T12:15:49.674453/Resupply - Democracy_Club__05May2022.tsv"
    )
    stations_name = (
        "2022-05-05/2022-03-29T12:15:49.674453/Resupply - Democracy_Club__05May2022.tsv"
    )
    elections = ["2022-05-05"]
    csv_encoding = "windows-1252"
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):
        # The Church of St John the Baptist, Broadway, Kidlington, Oxon
        if record.polling_place_id == "24883":
            record = record._replace(polling_place_easting="449651")
            record = record._replace(polling_place_northing="212578")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        if record.addressline6 in [
            "OX26 3EZ",
            "OX26 3EB",
            "OX16 9QF",
            "OX5 1LZ",
            "OX16 5AW",
            "OX27 7AE",
        ]:
            return None

        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10011889761",
            "100121291839",
            "10011906163",
        ]:
            return None

        return super().address_record_to_dict(record)
