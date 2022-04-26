from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "HAV"
    addresses_name = (
        "2022-05-05/2022-02-11T11:24:25.766169/Democracy_Club__05May2022.tsv"
    )
    stations_name = (
        "2022-05-05/2022-02-11T11:24:25.766169/Democracy_Club__05May2022.tsv"
    )
    elections = ["2022-05-05"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        if record.addressline6 in ["RM7 7BX", "RM11 2BY", "RM7 8DX", "RM12 4LG"]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):

        # Name change from council - don't carry forward
        # https://trello.com/c/Ig6nZ8NZ
        if record.polling_place_id == "9417":
            record = record._replace(polling_place_name="James Oglethorpe Pre-School")

        return super().station_record_to_dict(record)
