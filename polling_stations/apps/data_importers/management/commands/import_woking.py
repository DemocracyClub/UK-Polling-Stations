from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "WOI"
    addresses_name = (
        "2023-05-04/2023-03-05T11:18:57.001716/Democracy_Club__04May2023.tsv"
    )
    stations_name = (
        "2023-05-04/2023-03-05T11:18:57.001716/Democracy_Club__04May2023.tsv"
    )
    elections = ["2023-05-04"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "200000218826",  # THE BUNGALOW DAWNEY HILL, PIRBRIGHT
        ]:
            return None

        if record.addressline6 in ["KT14 6LT", "GU22 8AF"]:
            return None  # split

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # Horsell Evangelical Church High Street Horsell Woking GU21 3SZ
        if record.polling_place_id == "4943":
            record = record._replace(polling_place_postcode="GU21 4SZ")

        return super().station_record_to_dict(record)
