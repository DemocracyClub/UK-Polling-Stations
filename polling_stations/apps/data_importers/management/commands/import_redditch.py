from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "RED"
    addresses_name = "2021-04-23T10:48:03.563923/Democracy_Club__06May2021 Redditch.CSV"
    stations_name = "2021-04-23T10:48:03.563923/Democracy_Club__06May2021 Redditch.CSV"
    elections = ["2021-05-06"]

    def station_record_to_dict(self, record):
        if record.polling_place_id == "7070":
            # Matchborough Meeting Rooms
            # Misplaced; defer to AddressBase
            record = record._replace(
                polling_place_uprn="200002867453",
                polling_place_easting="",
                polling_place_northing="",
            )
        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "100120623245",
            "200003090064",
            "200003090054",
            "200003090054",
        ]:
            return None  # embedded in another district

        if record.addressline6 == "B67 6QA":
            # carried over postcode fix
            record = record._replace(addressline6="B97 6QA")

        if record.addressline6 in ["B98 8PX", "B97 6AQ"]:
            return None  # split

        return super().address_record_to_dict(record)
