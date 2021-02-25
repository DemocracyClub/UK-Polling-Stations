from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "FAR"
    addresses_name = (
        "2021-02-17T11:13:08.624493/Fareham BC Democracy_Club__06May2021.CSV"
    )
    stations_name = (
        "2021-02-17T11:13:08.624493/Fareham BC Democracy_Club__06May2021.CSV"
    )
    elections = ["2021-05-06"]
    csv_delimiter = ","
    csv_encoding = "windows-1252"

    def station_record_to_dict(self, record):

        if (
            record.polling_place_id == "6286"
        ):  # Titchfield Parish Rooms, High Street, Titchfield, Fareham, PO14 4AB
            record = record._replace(polling_place_postcode="PO14 4AQ")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)

        if record.post_code in [
            "SO31 7BJ",
            "PO16 7LR",
            "SO31 6BH",
            "PO14 4QS",
        ]:
            return None

        return rec
