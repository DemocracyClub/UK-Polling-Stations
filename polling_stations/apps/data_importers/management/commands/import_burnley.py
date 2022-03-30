from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "BUN"
    addresses_name = (
        "2022-05-05/2022-03-30T12:24:27.611217/Democracy_Club__05May2022.CSV"
    )
    stations_name = (
        "2022-05-05/2022-03-30T12:24:27.611217/Democracy_Club__05May2022.CSV"
    )
    elections = ["2022-05-05"]

    def station_record_to_dict(self, record):

        # Rosewood Primary School Moorland Road Entrance Burnley
        if record.polling_place_id == "5161":
            record = record._replace(polling_place_postcode="BB11 2PH")
            record = record._replace(polling_place_easting=383468)
            record = record._replace(polling_place_northing=431243)

        # St Matthews Church Hall Albion Street Burnley
        if record.polling_place_id == "5174":
            record = record._replace(polling_place_postcode="BB11 4JJ")
            record = record._replace(polling_place_easting=383312)
            record = record._replace(polling_place_northing=431998)

        # Dorset Street Entrance Rosegrove Infants School Dorset Street Burnley
        if record.polling_place_id == "5142":
            record = record._replace(polling_place_postcode="BB12 6HW")
            record = record._replace(polling_place_easting=381471)
            record = record._replace(polling_place_northing=432575)

        # Burnley Football Club 1882 Lounge Harry Potts Way Burnley
        if record.polling_place_id == "5265":
            record = record._replace(polling_place_postcode="BB10 4BX")

        # St Cuthbert`s Community Hall Sharp Street Burnley BB10 1UG
        if record.polling_place_id == "5246":
            record = record._replace(polling_place_postcode="BB10 1UJ")

        # Middlesex Over 50s Social Centre, Middlesex Avenue, Burnley
        if record.polling_place_id == "5287":
            record = record._replace(polling_place_postcode="BB12 6AA")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):

        if record.addressline6 in [
            "BB10 3BD",
            "BB10 3PF",
            "BB11 2QR",
            "BB12 8EH",
            "BB10 3JY",
            "BB10 2DT",
        ]:
            return None

        return super().address_record_to_dict(record)
