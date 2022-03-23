from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "WIN"
    addresses_name = (
        "2022-05-05/2022-03-23T16:46:37.210490/Democracy_Club__05May2022.tsv"
    )
    stations_name = (
        "2022-05-05/2022-03-23T16:46:37.210490/Democracy_Club__05May2022.tsv"
    )
    elections = ["2022-05-05"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):

        if record.addressline6 in [
            "SO24 9HZ",
            "SO32 1HP",
            "SO32 3PJ",
            "SO32 3LA",
        ]:
            return None
        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # Upham New Millennium Village Hall (Cttee Room)
        if record.polling_place_id == "10194":
            record = record._replace(polling_place_easting="452220")
            record = record._replace(polling_place_northing="119570")

        return super().station_record_to_dict(record)
