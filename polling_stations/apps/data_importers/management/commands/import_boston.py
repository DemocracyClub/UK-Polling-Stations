from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "BOT"
    addresses_name = (
        "2021-04-16T11:13:32.139850/Boston Democracy_Club__06May2021 (2).tsv"
    )
    stations_name = (
        "2021-04-16T11:13:32.139850/Boston Democracy_Club__06May2021 (2).tsv"
    )
    elections = ["2021-05-06"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        if record.addressline6 in [
            "PE21 7AL",
            "PE20 3AG",
            "PE21 8LA",
            "PE22 9JA",
            "PE22 9JW",
            "PE20 3QX",
            "PE21 0RL",
            "PE21 7LH",
            "PE22 9LJ",
            "PE21 7BJ",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):

        # St Thomas Church Hall London Road Boston PE21 8AG
        if record.polling_place_id == "4024":
            record = record._replace(polling_place_postcode="")

        return super().station_record_to_dict(record)
