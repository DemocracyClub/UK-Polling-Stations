from data_importers.ems_importers import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "FOE"
    addresses_name = (
        "2021-03-23T12:16:24.762200/Forest of Dean Democracy_Club__06May2021 (1).TSV"
    )
    stations_name = (
        "2021-03-23T12:16:24.762200/Forest of Dean Democracy_Club__06May2021 (1).TSV"
    )
    csv_delimiter = "\t"
    elections = ["2021-05-06"]

    def station_record_to_dict(self, record):
        if record.polling_place_name == "Rudford & Highleadon Village Hall":
            record = record._replace(
                polling_place_easting="377237",  # was 3777237
            )
        elif record.polling_place_name == "Primrose Hill Church Hall":
            record = record._replace(
                # Mistyped, but not going to work out what the right answer is.
                polling_place_easting="",
                polling_place_northing="",
                # should probably be GL15 5SL, but on wrong street, so let's just remove
                # it
                polling_place_postcode="",  # was GL15 5SF
                # Wrong UPRN too
                polling_place_uprn="",
            )

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        if record.addressline6 in [
            "GL15 6BP",
            "GL14 2PP",
            "GL14 2BB",
            "GL16 8QD",
            "GL17 9BE",
            "GL17 9JS",
            "GL17 9AL",
            "GL17 9QU",
            "GL15 4QH",
            "GL18 1AF",
            "GL15 4AN",
            "GL18 1LN",
            "GL18 1HJ",
            "GL16 8LN",
            "GL16 8JW",
            "GL15 4PU",
            "GL15 4RX",
        ]:
            return None  # split

        return super().address_record_to_dict(record)
