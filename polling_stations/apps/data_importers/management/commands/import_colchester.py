from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "COL"
    addresses_name = (
        "2025-02-20/2025-02-11T10:40:31.821365/Democracy_Club__20February2025.tsv"
    )
    stations_name = (
        "2025-02-20/2025-02-11T10:40:31.821365/Democracy_Club__20February2025.tsv"
    )
    elections = ["2025-02-20"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):
        # Tiptree United Reformed Church Hall, Chapel Road, Tiptree
        if record.polling_place_id == "14019":
            record = record._replace(
                polling_place_easting="590290", polling_place_northing="216096"
            )

        return super().station_record_to_dict(record)
