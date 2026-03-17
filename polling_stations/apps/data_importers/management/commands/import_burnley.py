from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "BUN"
    addresses_name = (
        "2026-05-07/2026-03-17T08:09:31.347670/Democracy_Club__07May2026.CSV"
    )
    stations_name = (
        "2026-05-07/2026-03-17T08:09:31.347670/Democracy_Club__07May2026.CSV"
    )
    elections = ["2026-05-07"]
    csv_encoding = "windows-1252"

    def station_record_to_dict(self, record):
        # postcode and coords correction for: Rosewood Primary School Moorland Road Entrance Burnley, BB11 2NY
        if record.polling_place_id == "6692":
            record = record._replace(polling_place_postcode="BB11 2PH")
            record = record._replace(polling_place_easting=383468)
            record = record._replace(polling_place_northing=431243)

        # postcode and coords correction for: St Matthews Church Hall Albion Street Burnley, BB11 4JG
        if record.polling_place_id == "6707":
            record = record._replace(polling_place_postcode="BB11 4JJ")
            record = record._replace(polling_place_easting=383312)
            record = record._replace(polling_place_northing=431998)

        # postcode and coords correction for: Dorset Street Entrance Rosegrove Infants School Dorset Street Burnley, BB12 6HT
        if record.polling_place_id == "6684":
            record = record._replace(polling_place_postcode="BB12 6HW")
            record = record._replace(polling_place_easting=381471)
            record = record._replace(polling_place_northing=432575)

        # extract postcode from address for: Padiham Road Methodist Church, Brassey Street, Burnley, BB12 8AD
        if record.polling_place_id in ["6760", "6786"]:
            record = record._replace(
                polling_place_postcode="BB12 8AD", polling_place_address_4=""
            )

        # extract postcode from address for: MAIN ENTRANCE, Burnley Campus, Barden Lane, Burnley, BB10 1JD
        if record.polling_place_id == "6756":
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
            "BB10 3PF",
            "BB11 2QR",
            "BB12 8EH",
            # suspect
            "BB10 1NY",
            "BB12 7EP",
            "BB12 7BW",
        ]:
            return None

        return super().address_record_to_dict(record)
