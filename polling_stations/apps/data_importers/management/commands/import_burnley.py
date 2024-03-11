from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "BUN"
    addresses_name = (
        "2024-05-02/2024-03-11T14:58:21.702385/Democracy_Club__02May2024 (15).tsv"
    )
    stations_name = (
        "2024-05-02/2024-03-11T14:58:21.702385/Democracy_Club__02May2024 (15).tsv"
    )
    elections = ["2024-05-02"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):
        # Rosewood Primary School Moorland Road Entrance Burnley
        if record.polling_place_id == "5756":
            record = record._replace(polling_place_postcode="BB11 2PH")
            record = record._replace(polling_place_easting=383468)
            record = record._replace(polling_place_northing=431243)

        # St Matthews Church Hall Albion Street Burnley
        if record.polling_place_id == "5744":
            record = record._replace(polling_place_postcode="BB11 4JJ")
            record = record._replace(polling_place_easting=383312)
            record = record._replace(polling_place_northing=431998)

        # Dorset Street Entrance Rosegrove Infants School Dorset Street Burnley
        if record.polling_place_id == "5786":
            record = record._replace(polling_place_postcode="BB12 6HW")
            record = record._replace(polling_place_easting=381471)
            record = record._replace(polling_place_northing=432575)

        # St Cuthbert`s Community Hall Sharp Street Burnley BB10 1UG
        if record.polling_place_id == "5669":
            record = record._replace(polling_place_postcode="BB10 1UJ")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10023761602",  # 7 SLADE LANE, PADIHAM, BURNLEY
        ]:
            return None

        if record.addressline6 in [
            # split
            "BB10 3JY",
            "BB11 2QR",
            "BB12 8EH",
            # suspect
            "BB10 1NY",
            "BB12 7EP",
            "BB12 7BW",
        ]:
            return None

        return super().address_record_to_dict(record)
