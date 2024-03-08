from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "SHN"
    addresses_name = (
        "2024-05-02/2024-03-08T16:27:14.461070/Democracy_Club__02May2024 - updated.tsv"
    )
    stations_name = (
        "2024-05-02/2024-03-08T16:27:14.461070/Democracy_Club__02May2024 - updated.tsv"
    )
    elections = ["2024-05-02"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):
        # Coordinate fixes from council:
        # Billinge St.Aidans Primary School, Off London Fields, Billinge, St Helens, WN5 7LS
        if record.polling_place_id == "5104":
            record = record._replace(
                polling_place_easting="353402",
                polling_place_northing="400375",
            )

        # Mobile at Fir Tree Farm, Pimbo Road, Rainford, WA11 8RG
        if record.polling_place_id == "5265":
            record = record._replace(
                polling_place_easting="350518",
                polling_place_northing="401287",
            )

        # Clock Face Miners Recreation Club, Crawford Street, Clock Face, St Helens
        if record.polling_place_id == "5095":
            record = record._replace(
                polling_place_easting="352927",
                polling_place_northing="391453",
            )
        # Chester Lane Library, Chester Lane, Sutton, St Helens, WA9 4DE
        if record.polling_place_id == "5099":
            record = record._replace(
                polling_place_easting="351948",
                polling_place_northing="391612",
            )

        # Mobile at Bird i'th Hand, Dunriding Lane, West Park, St Helens, WA10 3HE
        if record.polling_place_id == "5361":
            record = record._replace(
                polling_place_easting="349689",
                polling_place_northing="394757",
            )

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        if record.addressline6 in [
            # split
            "WA10 1HT",
            "WA9 3RR",
        ]:
            return None

        return super().address_record_to_dict(record)
