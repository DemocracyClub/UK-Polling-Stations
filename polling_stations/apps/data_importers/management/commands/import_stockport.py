from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "SKP"
    addresses_name = (
        "2022-05-05/2022-03-02T15:12:55.643036/Democracy_Club__05May2022.tsv"
    )
    stations_name = (
        "2022-05-05/2022-03-02T15:12:55.643036/Democracy_Club__05May2022.tsv"
    )
    elections = ["2022-05-05"]
    csv_encoding = "windows-1252"
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):

        if record.addressline6 in [
            "SK8 3TJ",
            "SK6 7DH",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # Kingsway School (Lower) Broadway Campus High Grove Road Cheadle SK8 1NP
        if record.polling_place_id == "10415":
            record = record._replace(polling_place_easting="")
            record = record._replace(polling_place_northing="")

        # Mobile Polling Station, Junction of Broadway and Beauvale Avenue, Offerton SK2 6SF
        if record.polling_place_id == "11293":
            record = record._replace(polling_place_postcode="SK2 5SF")

        return super().station_record_to_dict(record)
