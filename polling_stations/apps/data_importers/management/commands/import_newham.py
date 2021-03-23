from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "NWM"
    addresses_name = "2021-03-22T13:30:16.944061/Democracy_Club__06May2021.CSV"
    stations_name = "2021-03-22T13:30:16.944061/Democracy_Club__06May2021.CSV"
    elections = ["2021-05-06"]

    def station_record_to_dict(self, record):
        # Fix from: 890908:polling_stations/apps/data_importers/management/commands/misc_fixes.py:224
        # Carpenters and Docklands Centre 98 Gibbins Road Stratford London
        if record.polling_place_id == "5614":
            record = record._replace(polling_place_easting="538526.11")
            record = record._replace(polling_place_northing="184252.81")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "46003425",  # 499A BARKING ROAD, LONDON
            "10090756873",  # FLAT 1 23 NOTTINGHAM AVENUE, WEST BECKTON, LONDON
            "10009012301",  # 140B BARKING ROAD, LONDON
            "10034508484",  # FLAT ABOVE 33 VICARAGE LANE, EAST HAM, LONDON
            "10009012905",  # 62A TREE ROAD, WEST BECKTON, LONDON
            "10008988958",
            "10094371250",
        ]:
            return None  # in an otherwise multiple station postcode, so safe to remove

        return super().address_record_to_dict(record)
