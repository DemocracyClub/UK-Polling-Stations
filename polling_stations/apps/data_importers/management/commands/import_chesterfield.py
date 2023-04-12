from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "CHS"
    addresses_name = (
        "2023-05-04/2023-04-12T16:11:40.810471/Democracy_Club__04May2023.tsv"
    )
    stations_name = (
        "2023-05-04/2023-04-12T16:11:40.810471/Democracy_Club__04May2023.tsv"
    )
    elections = ["2023-05-04"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "74088505",  # 11B NEWBRIDGE LANE, BRIMINGTON
            "74068238",  # THE PADDOCKS, CROW LANE, CHESTERFIELD
            "74006059",  # DOBBIN CLOUGH FARM, CROW LANE, CHESTERFIELD
            "74078771",  # 84 SALTERGATE, CHESTERFIELD
        ]:
            return None

        if record.addressline6 in [
            # splits
            "S40 3LA",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # Christ Church Primary School, Tapton View Road, Chesterfield, S41 1JU
        # Proposed correction: S41 7JU
        if record.polling_place_id == "6915":
            record = record._replace(polling_place_postcode="")

        return super().station_record_to_dict(record)
