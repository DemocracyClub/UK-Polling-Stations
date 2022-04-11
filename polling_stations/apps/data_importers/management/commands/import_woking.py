from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "WOI"
    addresses_name = (
        "2022-05-05/2022-04-11T14:04:40.495448/Democracy_Club__05May2022.tsv"
    )
    stations_name = (
        "2022-05-05/2022-04-11T14:04:40.495448/Democracy_Club__05May2022.tsv"
    )
    elections = ["2022-05-05"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "200000218826",  # THE BUNGALOW DAWNEY HILL, PIRBRIGHT
            "10002428855",  # FLAT 7, THE OLD BREW HOUSE 130-132, HIGH STREET, OLD WOKING, WOKING
            "10002428856",  # FLAT 8, THE OLD BREW HOUSE 130-132, HIGH STREET, OLD WOKING, WOKING"
        ]:
            return None

        if record.addressline6 in ["KT14 6LT", "GU22 8AF"]:
            return None  # split

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # Horsell Evangelical Church High Street Horsell Woking GU21 3SZ
        if record.polling_place_id == "4392":
            record = record._replace(polling_place_postcode="GU21 4SZ")

        return super().station_record_to_dict(record)
