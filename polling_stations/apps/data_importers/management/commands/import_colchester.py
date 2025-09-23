from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "COL"
    addresses_name = (
        "2025-10-23/2025-09-15T11:51:43.956849/Democracy_Club__23October2025.tsv"
    )
    stations_name = (
        "2025-10-23/2025-09-15T11:51:43.956849/Democracy_Club__23October2025.tsv"
    )
    elections = ["2025-10-23"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):
        # Roman Circus Visitor Centre Roman Circus Walk Colchester CO2 7GZ
        if record.polling_place_id == "14126":
            record = record._replace(polling_place_uprn="10024406304")

        # Salvation Army Citadel Butt Road Colchester CO3 3DA
        if record.polling_place_id == "14131":
            record = record._replace(polling_place_uprn="10004953252")

        return super().station_record_to_dict(record)
