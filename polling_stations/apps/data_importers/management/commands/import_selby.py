from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "SEL"
    addresses_name = "2021-11-08T12:18:21.900777/Democracy_Club__25November2021.tsv"
    stations_name = "2021-11-08T12:18:21.900777/Democracy_Club__25November2021.tsv"
    elections = ["2021-11-25"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        if record.addressline6 in [
            "YO8 8FH",
            "YO8 3EH",
            "LS24 9HH",
            "YO8 3ED",
            "LS253AU",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):

        # Lady Popplewell Centre Beechwood Close Sherburn in Elmet Leeds LS25 6HO
        if record.polling_place_id == "6162":
            record = record._replace(polling_place_postcode="LS25 6HU")

        return super().station_record_to_dict(record)
