from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "SOX"
    addresses_name = "2023-05-04/2023-03-06T12:18:16.065364/South Oxfordshire District Council - Democracy_Club__04May2023.TSV"
    stations_name = "2023-05-04/2023-03-06T12:18:16.065364/South Oxfordshire District Council - Democracy_Club__04May2023.TSV"
    elections = ["2023-05-04"]
    csv_encoding = "windows-1252"
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        if record.addressline6 in [
            "OX11 7TP",
            "OX11 7SE",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # Thame Snooker Club 1a Saint Andrew Court Wellington Street Thame OX9 3WT
        if record.polling_place_id == "15012":
            record = record._replace(polling_place_easting="")
            record = record._replace(polling_place_northing="")

        return super().station_record_to_dict(record)
