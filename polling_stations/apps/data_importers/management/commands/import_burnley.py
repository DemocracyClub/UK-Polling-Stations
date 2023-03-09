from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "BUN"
    addresses_name = (
        "2023-05-04/2023-03-15T16:01:16.960415/Democracy_Club__04May2023.CSV"
    )
    stations_name = (
        "2023-05-04/2023-03-15T16:01:16.960415/Democracy_Club__04May2023.CSV"
    )
    elections = ["2023-05-04"]

    def station_record_to_dict(self, record):
        # Rosewood Primary School Moorland Road Entrance Burnley
        if record.polling_place_id == "5399":
            record = record._replace(polling_place_postcode="BB11 2PH")
            record = record._replace(polling_place_easting=383468)
            record = record._replace(polling_place_northing=431243)

        # St Matthews Church Hall Albion Street Burnley
        if record.polling_place_id == "5413":
            record = record._replace(polling_place_postcode="BB11 4JJ")
            record = record._replace(polling_place_easting=383312)
            record = record._replace(polling_place_northing=431998)

        # Dorset Street Entrance Rosegrove Infants School Dorset Street Burnley
        if record.polling_place_id == "5379":
            record = record._replace(polling_place_postcode="BB12 6HW")
            record = record._replace(polling_place_easting=381471)
            record = record._replace(polling_place_northing=432575)

        # St Cuthbert`s Community Hall Sharp Street Burnley BB10 1UG
        if record.polling_place_id == "5484":
            record = record._replace(polling_place_postcode="BB10 1UJ")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        if record.addressline6 in [
            "BB10 3JY",
            "BB10 3PF",
            "BB10 3BD",
            "BB12 8EH",
            "BB11 2QR",
        ]:
            return None

        return super().address_record_to_dict(record)
