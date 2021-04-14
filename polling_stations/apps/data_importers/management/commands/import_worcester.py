from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "WOC"
    addresses_name = (
        "2021-03-26T11:04:20.460985/Worcester Democracy_Club__06May2021 (1).CSV"
    )
    stations_name = (
        "2021-03-26T11:04:20.460985/Worcester Democracy_Club__06May2021 (1).CSV"
    )
    elections = ["2021-05-06"]
    csv_delimiter = ","

    def address_record_to_dict(self, record):
        if record.addressline6 in [
            "WR1 1HT",
            "WR1 1DF",
            "WR5 3EP",
            "WR5 3ES",
            "WR1 2AH",
            "WR3 8SB",
            "WR4 9BG",
            "WR3 8ET",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):

        # Polling station B3 Marquee Blessed Edward College rear car park Access via Evendine Close Worcester
        # set to same location as polling station B2 Marquee Blessed Edward College rear car park Access via Evendine Close Worcester
        if record.polling_place_id == "6014":
            record = record._replace(polling_place_easting="385795")
            record = record._replace(polling_place_northing="253608")

        # Polling Station 2 Hall 1 Lyppard Hub Ankerage Green, Off Millwood Drive
        # set to same postcode as Polling Station 3 Hall 1 Lyppard Hub Ankerage Green, Off Millwood Drive Worcester
        if record.polling_place_id == "6016":
            record = record._replace(polling_place_postcode="WR4 0DZ")

        return super().station_record_to_dict(record)
