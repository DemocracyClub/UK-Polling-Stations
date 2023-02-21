from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "KIR"
    addresses_name = (
        "2022-05-05/2022-04-01T09:37:46.018185/NEWDemocracy_Club__05May2022.tsv"
    )
    stations_name = (
        "2022-05-05/2022-04-01T09:37:46.018185/NEWDemocracy_Club__05May2022.tsv"
    )
    elections = ["2022-05-05"]
    csv_encoding = "windows-1252"
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):
        # Cleckheaton Methodist Church, Greenside Cleckheaton
        if record.polling_place_id == "14951":
            record = record._replace(polling_place_easting="")
            record = record._replace(polling_place_northing="")

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
