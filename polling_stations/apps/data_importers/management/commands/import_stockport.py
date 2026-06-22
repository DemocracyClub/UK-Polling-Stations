from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "SKP"
    addresses_name = (
        "2026-07-30/2026-06-22T16:49:19.273784/Democracy_Club__30July2026.tsv"
    )
    stations_name = (
        "2026-07-30/2026-06-22T16:49:19.273784/Democracy_Club__30July2026.tsv"
    )
    elections = ["2026-07-30"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "100011502976",  # 43 MAULDETH ROAD, STOCKPORT
            "100011431101",  # 42A CHURCH ROAD, GATLEY, CHEADLE
            "100012482785",  # YEW TREE FARM, OFFERTON ROAD, STOCKPORT
            "10090543093",  # YEW TREE FARM BARN OFFERTON ROAD, OFFERTON, STOCKPORT
            "100012482780",  # HIGH TREES, OFFERTON ROAD, STOCKPORT
        ]:
            return None

        if record.addressline6 in [
            # splits
            "SK3 9HB",
            "SK4 5BS",
            "SK6 2BD",
            "SK6 6LP",
            "SK7 1JX",
            "SK7 3DQ",
            "SK7 4NX",
            "SK8 4BU",
            # looks wrong
            "SK6 7AY",
        ]:
            return None

        return super().address_record_to_dict(record)
