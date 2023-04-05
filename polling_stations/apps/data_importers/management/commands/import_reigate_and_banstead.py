from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "REI"
    addresses_name = (
        "2023-05-04/2023-04-05T12:04:27.040829/Democracy_Club__04May2023.tsv"
    )
    stations_name = (
        "2023-05-04/2023-04-05T12:04:27.040829/Democracy_Club__04May2023.tsv"
    )
    elections = ["2023-05-04"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):
        # Woodmansterne Village Hall, Carshalton Road, Woodmansterne, Banstead, Surrey
        if record.polling_place_id == "4916":
            record = record._replace(
                polling_place_easting="527572", polling_place_northing="160117"
            )

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.property_urn.lstrip("0")

        if uprn in [
            "68181592",  # 2A PARKHURST ROAD, HORLEY
        ]:
            return None

        return super().address_record_to_dict(record)
