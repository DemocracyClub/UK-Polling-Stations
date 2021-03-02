from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "MOL"
    addresses_name = (
        "2021-03-02T12:34:43.331647/Mole Valley Democracy_Club__06May2021 (1).tsv"
    )
    stations_name = (
        "2021-03-02T12:34:43.331647/Mole Valley Democracy_Club__06May2021 (1).tsv"
    )
    elections = ["2021-05-06"]
    csv_delimiter = "\t"
    csv_encoding = "windows-1252"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10000828460",  # 26A OTTWAYS LANE, ASHTEAD
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # Catholic Church Hall, (Main Hall) of our Lady & St Peter, Copthorne Road, Leatherhead
        if record.polling_place_id == "4783":
            record = record._replace(polling_place_postcode="KT22 7EZ")

        # Pippbrook (Council Offices), Reigate Road, Dorking, (Entrance Behind Bus Stop)
        if record.polling_place_id == "4630":
            record = record._replace(polling_place_postcode="RH4 1SJ")

        # Wotton Village Hall Guildford Road Wotton RH5 6QQ - change of station
        if record.polling_place_id == "4684":
            record = record._replace(
                polling_place_name="Wotton House",
                polling_place_address_1="Guilford Road",
                polling_place_address_2="Dorking",
                polling_place_address_3="Surrey",
                polling_place_postcode="RH5 6HS",
            )

        return super().station_record_to_dict(record)
