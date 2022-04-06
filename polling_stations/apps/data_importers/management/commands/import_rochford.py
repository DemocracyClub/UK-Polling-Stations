from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "ROC"
    addresses_name = (
        "2022-05-05/2022-04-06T10:59:20.095915/Democracy_Club__05May2022-5.tsv"
    )
    stations_name = (
        "2022-05-05/2022-04-06T10:59:20.095915/Democracy_Club__05May2022-5.tsv"
    )
    elections = ["2022-05-05"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):

        # Wesley Room, Methodist Church Hall
        if record.polling_place_id == "5391":
            record = record._replace(polling_place_postcode="SS6 7JP")

        # user error report #208
        # Grange Free Church
        if record.polling_place_id == "5538":
            record = record._replace(polling_place_easting="0")
            record = record._replace(polling_place_northing="0")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):

        if record.addressline6 in [
            "SS3 0LQ",
            "SS6 8DF",
            "SS3 0HH",
        ]:
            return None

        return super().address_record_to_dict(record)
