from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "TEI"
    addresses_name = (
        "2023-05-04/2023-03-10T11:50:22.113903/Democracy_Club__04May2023.tsv"
    )
    stations_name = (
        "2023-05-04/2023-03-10T11:50:22.113903/Democracy_Club__04May2023.tsv"
    )
    elections = ["2023-05-04"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):
        # Alice Cross Day Centre
        if record.polling_place_id == "8273":
            record = record._replace(polling_place_easting="293930")
            record = record._replace(polling_place_northing="73047")

        if record.polling_place_id == "8292":
            record = record._replace(polling_place_postcode="")

        return super().station_record_to_dict(record)

    #
    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10032954133",  # BARN COTTAGE, HIGHER BRIMLEY, BOVEY TRACEY, NEWTON ABBOT
            "100041145017",  # GLENDARAGH, EXETER ROAD, DAWLISH
        ]:
            return None

        if record.addressline6 in [
            "TQ13 9TR",
            "TQ14 8NL",
            "TQ13 9YW",
            "TQ14 9LZ",
            "EX7 9PL",
            "TQ14 8FW",
            "TQ13 7BU",
            "TQ12 1HR",
            "TQ14 9AZ",
            "TQ14 9AA",
            "TQ13 9NW",
        ]:
            return None

        return super().address_record_to_dict(record)
