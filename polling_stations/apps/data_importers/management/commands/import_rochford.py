from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "ROC"
    addresses_name = (
        "2024-05-02/2024-04-10T16:39:43.413423/Democracy_Club__02May2024.tsv"
    )
    stations_name = (
        "2024-05-02/2024-04-10T16:39:43.413423/Democracy_Club__02May2024.tsv"
    )
    elections = ["2024-05-02"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10010561894",  # THE PADDOCKS, VANDERBILT AVENUE, RAYLEIGH
            "100090592879",  # 157 STAMBRIDGE ROAD, ROCHFORD
            "100091264335",  # BARROW HALL FARMHOUSE BARROW HALL ROAD, LITTLE WAKERING
            "100090595184",  # 56 LITTLE WAKERING ROAD, GREAT WAKERING, SOUTHEND-ON-SEA
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
        if record.polling_place_id == "6131":
            record = record._replace(polling_place_postcode="SS6 7JP")

        # Rayleigh Vineyard Church, London Road, Rayleigh, Essex SS6 9AY
        if record.polling_place_id == "6100":
            record = record._replace(polling_place_northing="191478")

        return super().station_record_to_dict(record)
