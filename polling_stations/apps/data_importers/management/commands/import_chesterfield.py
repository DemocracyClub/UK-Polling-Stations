from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "CHS"
    addresses_name = (
        "2025-05-01/2025-03-12T13:24:59.688646/Democracy_Club__01May2025.tsv"
    )
    stations_name = (
        "2025-05-01/2025-03-12T13:24:59.688646/Democracy_Club__01May2025.tsv"
    )
    elections = ["2025-05-01"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "74068238",  # THE PADDOCKS, CROW LANE, CHESTERFIELD
            "74006059",  # DOBBIN CLOUGH FARM, CROW LANE, CHESTERFIELD
        ]:
            return None

        if record.addressline6 in [
            # split
            "S40 3LA",
            # suspect
            "S40 2AL",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # postcode correction for: Christ Church Primary School, Tapton View Road, Chesterfield, S41 1JU
        # postcode is also in a wrong column
        if record.polling_place_id == "8292":
            record = record._replace(
                polling_place_postcode="S41 7JU", polling_place_address_3=""
            )

        return super().station_record_to_dict(record)
