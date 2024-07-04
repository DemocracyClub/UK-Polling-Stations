from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "SND"
    addresses_name = (
        "2024-07-04/2024-06-06T10:15:05.242461/Democracy_Club__04July2024.CSV"
    )
    stations_name = (
        "2024-07-04/2024-06-06T10:15:05.242461/Democracy_Club__04July2024.CSV"
    )
    elections = ["2024-07-04"]

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "45002135",  # SUNHILL, NORTH ROAD, HETTON-LE-HOLE, HOUGHTON LE SPRING
        ]:
            return None

        if record.addressline6 in [
            # split
            "DH4 7RD",
            "DH4 5HY",
            "SR2 0LE",
            "SR4 8JF",
            "SR4 7SD",
            "SR5 3EP",
            "SR2 9JG",
            "SR2 0AQ",
            "DH4 4JH",
            "SR2 8RA",
            "SR6 9DY",
            "SR4 0BT",
            "SR2 7HZ",
            "SR4 8JU",
            "SR4 6NP",
            "SR3 1XF",
            "SR3 3QH",
            "SR6 0NB",
            "SR4 8HA",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # removes map for: Sulgrave Centre Manor Road Sulgrave Washington
        if record.polling_place_id == "19371":
            record = record._replace(
                polling_place_easting="431374",
                polling_place_northing="558024",
            )

        return super().station_record_to_dict(record)
