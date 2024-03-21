from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "HIG"
    addresses_name = (
        "2024-05-02/2024-03-21T13:43:41.849663/Democracy_Club__02May2024 (21).tsv"
    )
    stations_name = (
        "2024-05-02/2024-03-21T13:43:41.849663/Democracy_Club__02May2024 (21).tsv"
    )
    elections = ["2024-05-02"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10010727932",  # HOCKERLEY HALL FARM, HOCKERLEY LANE, WHALEY BRIDGE, HIGH PEAK
            "10010747214",  # THE BUNGALOW, HARPUR HILL BUSINESS PARK, BUXTON
            "10010715355",  # RED GAP FARM, GREEN FAIRFIELD, BUXTON
            "10010720655",  # BLACK HILLGATE FARM, KETTLESHULME, HIGH PEAK
            "10010751272",  # MILTON FARMHOUSE, CHAPEL MILTON, CHAPEL-EN-LE-FRITH, HIGH PEAK
        ]:
            return None

        if record.addressline6 in [
            # splits
            "S33 0AB",
            "SK23 6BR",
            # suspect
            "SK22 3DU",  # LARKHILL TERRACE, NEW MILLS, HIGH PEAK
            "SK22 1BW",  # CRESCENT ROW, BIRCH VALE
        ]:
            return None

        return super().address_record_to_dict(record)
