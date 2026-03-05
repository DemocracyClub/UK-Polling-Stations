from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "ROC"
    addresses_name = (
        "2026-05-07/2026-03-05T09:15:56.599490/Democracy_Club__07May2026.tsv"
    )
    stations_name = (
        "2026-05-07/2026-03-05T09:15:56.599490/Democracy_Club__07May2026.tsv"
    )
    elections = ["2026-05-07"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10010561894",  # THE PADDOCKS, VANDERBILT AVENUE, RAYLEIGH
            "100090592879",  # 157 STAMBRIDGE ROAD, ROCHFORD
            "100091264335",  # BARROW HALL FARMHOUSE BARROW HALL ROAD, LITTLE WAKERING
            "100090595184",  # 56 LITTLE WAKERING ROAD, GREAT WAKERING, SOUTHEND-ON-SEA
            "100090575372",  # 4 TYRELLS, HOCKLEY
        ]:
            return None

        if record.addressline6 in [
            # split
            "SS3 0LQ",
            "SS3 0HH",
            "SS6 8DF",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # Wesley Room, Methodist Church Hall, Eastwood Road, Rayleigh, Essex
        # Fixing the warning, correction is safe
        if record.polling_place_id == "7106":
            record = record._replace(polling_place_postcode="SS6 7JP")

        return super().station_record_to_dict(record)
