from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "KIN"
    addresses_name = (
        "2023-05-04/2023-03-13T16:05:14.621201/Democracy_Club__04May2023.tsv"
    )
    stations_name = (
        "2023-05-04/2023-03-13T16:05:14.621201/Democracy_Club__04May2023.tsv"
    )
    elections = ["2023-05-04"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):
        # Family Entertainment Centre, Blue Bull Cafe Bar
        if record.polling_place_id == "23301":
            record = record._replace(
                polling_place_easting="", polling_place_northing=""
            )

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10000033946",  # 81B HIGH STREET, KING'S LYNN
        ]:
            return None
        if record.addressline6 in [
            # split
            "PE34 3BJ",
            "PE31 6HJ",
            # look wrong
            "PE30 1JG",
        ]:
            return None

        return super().address_record_to_dict(record)
