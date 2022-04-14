from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "SCA"
    addresses_name = (
        "2022-05-05/2022-03-09T15:38:47.461320/Democracy_Club__05May2022.tsv"
    )
    stations_name = (
        "2022-05-05/2022-03-09T15:38:47.461320/Democracy_Club__05May2022.tsv"
    )
    elections = ["2022-05-05"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):
        # Station change from council
        if record.polling_place_id == "8757":
            record = record._replace(
                polling_place_name="St John the Evangelist Church",
                polling_place_address_1="Church Road",
                polling_place_address_2="Little Wilbraham",
                polling_place_address_3="",
                polling_place_address_4="Cambridge",
                polling_place_postcode="CB21 5LE",
            )

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):

        if record.addressline6 in [
            "CB24 3DS",
            "CB23 3UG",
            "SG8 0BD",
            "CB21 5LF",
            "CB23 1AA",
            "CB22 5AN",
        ]:
            return None

        return super().address_record_to_dict(record)
