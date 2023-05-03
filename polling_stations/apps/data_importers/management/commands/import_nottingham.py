from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "NGM"
    addresses_name = (
        "2023-05-04/2023-04-05T16:34:11.754241/Democracy_Club__04May2023.tsv"
    )
    stations_name = (
        "2023-05-04/2023-04-05T16:34:11.754241/Democracy_Club__04May2023.tsv"
    )
    elections = ["2023-05-04"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        if record.addressline6 in [
            # split
            "NG7 1BZ",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # Council Station Change https://trello.com/c/Z7H14XBS
        # Mariner Court Common Room -> Crabtree Farm Community Centre
        if record.polling_place_id == "6853":
            record = record._replace(
                polling_place_name="Crabtree Farm Community Centre",
                polling_place_address_1="Steadfold Close",
                polling_place_address_2="",
                polling_place_address_3="",
                polling_place_address_4="Nottingham",
                polling_place_postcode="NG6 8AX",
            )
        return super().station_record_to_dict(record)
