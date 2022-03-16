from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "WOK"
    addresses_name = (
        "2022-05-05/2022-03-16T15:20:21.336512/Democracy_Club__05May2022.tsv"
    )
    stations_name = (
        "2022-05-05/2022-03-16T15:20:21.336512/Democracy_Club__05May2022.tsv"
    )
    elections = ["2022-05-05"]
    csv_encoding = "windows-1252"
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "14008163",  # LOWER COTTAGE, WHITE HORSE LANE, FINCHAMPSTEAD, WOKINGHAM
        ]:
            return None

        if record.addressline6 in [
            "RG6 4AG",
            "RG7 1NL",
            "RG10 9HN",
            "RG7 1TB",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):

        # Civic Offices Shute End Wokingham Berkshire RG40 1WH
        if record.polling_place_id == "2891":
            record = record._replace(polling_place_postcode="")

        return super().station_record_to_dict(record)
