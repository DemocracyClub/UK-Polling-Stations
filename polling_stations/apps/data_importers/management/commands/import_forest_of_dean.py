from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "FOE"
    addresses_name = (
        "2023-05-04/2023-03-09T18:08:54.956552/Democracy_Club__04May2023.tsv"
    )
    stations_name = (
        "2023-05-04/2023-03-09T18:08:54.956552/Democracy_Club__04May2023.tsv"
    )
    elections = ["2023-05-04"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):
        if record.polling_place_name == "Rudford & Highleadon Village Hall":
            record = record._replace(
                polling_place_easting="377237",  # was 3777237
            )
        elif record.polling_place_id == "1685":
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
        if record.property_urn in [
            "10090651915",
            "10014327870",
        ]:
            return None

        if record.addressline6 in [
            "GL15 4QH",
            "GL14 2BB",
            "GL14 2HQ",
            "GL17 9JS",
            "GL17 9QU",
            "GL14 2PP",
            "GL15 4AN",
            "GL18 1LN",
        ]:
            return None  # split

        return super().address_record_to_dict(record)
