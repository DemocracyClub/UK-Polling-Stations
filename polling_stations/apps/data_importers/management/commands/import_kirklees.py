from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "KIR"
    addresses_name = (
        "2022-05-05/2022-03-10T15:06:01.054793/Democracy_Club__05May2022.tsv"
    )
    stations_name = (
        "2022-05-05/2022-03-10T15:06:01.054793/Democracy_Club__05May2022.tsv"
    )
    elections = ["2022-05-05"]
    csv_encoding = "windows-1252"
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):
        # Cleckheaton Methodist Church, Greenside Cleckheaton
        if record.polling_place_id == "14951":
            record = record._replace(polling_place_easting="")
            record = record._replace(polling_place_northing="")

        # Pre-School Room - Lydgate J & I School, Lydgate Road, Soothill
        if record.polling_place_id == "14866":
            record = record._replace(polling_place_easting="")
            record = record._replace(polling_place_northing="")

        # Marsden United Reform Church, Peel Street, Marsden
        if record.polling_place_id == "15516":
            record = record._replace(polling_place_easting="")
            record = record._replace(polling_place_northing="")
            record = record._replace(polling_place_uprn="")

        # Roberttown Community Centre
        # Entrance is on Church Rd
        if record.polling_place_id == "14258":
            record = record._replace(polling_place_easting="419480")
            record = record._replace(polling_place_northing="422649")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):

        if record.addressline6 in [
            "HD9 7EH",
            "HD7 5XB",
        ]:
            return None

        return super().address_record_to_dict(record)
