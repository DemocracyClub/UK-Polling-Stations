from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "SHN"
    addresses_name = (
        "2024-05-02/2024-02-26T16:10:35.670143/Democracy_Club__02May2024.tsv"
    )
    stations_name = (
        "2024-05-02/2024-02-26T16:10:35.670143/Democracy_Club__02May2024.tsv"
    )
    elections = ["2024-05-02"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):
        # Crank Recreation Ground, Crank Hill, Crank, Rainford WA11 7SD
        if record.polling_place_id == "5261":
            record = record._replace(
                polling_place_easting="350545",
                polling_place_northing="399665",
            )

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        if record.addressline6 in [
            # split
            "WA10 1HT",
            "WA9 3RR",
        ]:
            return None

        return super().address_record_to_dict(record)
