from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "BUN"
    addresses_name = (
        "2025-05-01/2025-02-27T11:43:17.412314/Democracy_Club__01May2025.tsv"
    )
    stations_name = (
        "2025-05-01/2025-02-27T11:43:17.412314/Democracy_Club__01May2025.tsv"
    )
    elections = ["2025-05-01"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):
        # postcode and coords correction for: Rosewood Primary School Moorland Road Entrance Burnley, BB11 2NY
        if record.polling_place_id == "6149":
            record = record._replace(polling_place_postcode="BB11 2PH")
            record = record._replace(polling_place_easting=383468)
            record = record._replace(polling_place_northing=431243)

        # postcode and coords correction for: St Matthews Church Hall Albion Street Burnley, BB11 4JG
        if record.polling_place_id == "6117":
            record = record._replace(polling_place_postcode="BB11 4JJ")
            record = record._replace(polling_place_easting=383312)
            record = record._replace(polling_place_northing=431998)

        # postcode and coords correction for: Dorset Street Entrance Rosegrove Infants School Dorset Street Burnley, BB12 6HT
        if record.polling_place_id == "6173":
            record = record._replace(polling_place_postcode="BB12 6HW")
            record = record._replace(polling_place_easting=381471)
            record = record._replace(polling_place_northing=432575)

        # postcode correction for: St Cuthbert`s Community Hall Sharp Street Burnley, BB10 1UG
        if record.polling_place_id == "6307":
            record = record._replace(polling_place_postcode="BB10 1UJ")

        # extract postcode from address for: Padiham Road Methodist Church, Brassey Street, Burnley, BB12 8AD
        if record.polling_place_id in ["6142", "6130"]:
            record = record._replace(
                polling_place_postcode="BB12 8AD", polling_place_address_4=""
            )

        # extract postcode from address for: MAIN ENTRANCE, Burnley Campus, Barden Lane, Burnley, BB10 1JD
        if record.polling_place_id == "6315":
            record = record._replace(
                polling_place_postcode="BB10 1JD", polling_place_address_4=""
            )

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
