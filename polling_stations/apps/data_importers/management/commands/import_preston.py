from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "PRE"
    addresses_name = (
        "2022-05-05/2022-03-25T10:08:40.592532/Democracy_Club__05May2022.tsv"
    )
    stations_name = (
        "2022-05-05/2022-03-25T10:08:40.592532/Democracy_Club__05May2022.tsv"
    )
    elections = ["2022-05-05"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):
        if record.polling_place_id in [
            "4167",  # Millennium Hall
            "4223",  # Goosnargh Village Hall
        ]:
            record = record._replace(
                polling_place_easting="", polling_place_northing=""
            )

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in ["10093760928", "100010579401", "100010574023"]:
            return None

        if record.addressline6 in []:
            return None

        return super().address_record_to_dict(record)
