from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "CHS"
    addresses_name = (
        "2024-07-04/2024-06-05T14:34:42.061867/Democracy_Club__04July2024.tsv"
    )
    stations_name = (
        "2024-07-04/2024-06-05T14:34:42.061867/Democracy_Club__04July2024.tsv"
    )
    elections = ["2024-07-04"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "74068238",  # THE PADDOCKS, CROW LANE, CHESTERFIELD
            "74006059",  # DOBBIN CLOUGH FARM, CROW LANE, CHESTERFIELD
            "74078771",  # 84 SALTERGATE, CHESTERFIELD
            "74026116",  # HILL TOP, HALL LANE, STAVELEY, CHESTERFIELD
        ]:
            return None

        if record.addressline6 in [
            # split
            "S40 3LA",
            # suspect
            "S40 2AL",
            "S41 9RL",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # postcode correction for: Christ Church Primary School, Tapton View Road, Chesterfield, S41 1JU
        # postcode is also in a wrong column
        if record.polling_place_id == "7624":
            record = record._replace(
                polling_place_postcode="S41 7JU", polling_place_address_3=""
            )

        # postcode correction for: Hasland Methodist Church, Hampton Street, Hasland, Chesterfield, S41 1LH
        if record.polling_place_id == "7577":
            record = record._replace(polling_place_postcode="S41 0LH")

        return super().station_record_to_dict(record)
