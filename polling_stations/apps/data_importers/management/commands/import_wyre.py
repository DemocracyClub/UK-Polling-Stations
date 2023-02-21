from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "WYR"
    addresses_name = "2021-02-15T11:25:19.329853/Wyre Democracy_Club__06May2021.CSV"
    stations_name = "2021-02-15T11:25:19.329853/Wyre Democracy_Club__06May2021.CSV"
    elections = ["2021-05-06"]
    csv_delimiter = ","
    csv_encoding = "windows-1252"

    def station_record_to_dict(self, record):
        if record.polling_place_id == "4304":  # Charles Saer Community Primary School
            record = record._replace(polling_place_postcode="FY7 8DD")

        if (
            record.polling_place_id == "4295"
        ):  # Senior Citizens Assoc Hall, 190 Victoria Road West, Thornton Cleveleys - FY5 7JA ==> FY5 3NG
            record = record._replace(polling_place_postcode="FY5 3NG")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if record.post_code in [
            "FY6 8FS",  # Astray postcode
            "FY6 7GH",  # Astray postcode
            "FY7 6FJ",  # Astray postcode
            "PR3 1TS",  # Astray postcode
            "FY5 3LS",  # Postcode split over large distance
            "FY6 9EX",  # Postcode split over large distance
        ]:
            return None

        if uprn in [
            "10034088556",  # FLAT AT GREAT SEASONS GARSTANG BYPASS ROAD, GARSTANG, PR3 1PH
            "10093998387",  # 97A CROSTON ROAD, GARSTANG, PR3 0HQ - postcode likely should be PR3 1HQ
        ]:
            return None

        return rec
