from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "HIG"
    addresses_name = (
        "2023-05-04/2023-04-12T16:06:53.275227/Democracy_Club__04May2023.tsv"
    )
    stations_name = (
        "2023-05-04/2023-04-12T16:06:53.275227/Democracy_Club__04May2023.tsv"
    )
    elections = ["2023-05-04"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10010727932",  # HOCKERLEY HALL FARM, HOCKERLEY LANE, WHALEY BRIDGE, HIGH PEAK
            "10010747214",  # THE BUNGALOW, HARPUR HILL BUSINESS PARK, BUXTON
            "10010715355",  # RED GAP FARM, GREEN FAIRFIELD, BUXTON
            "10010720655",  # BLACK HILLGATE FARM, KETTLESHULME, HIGH PEAK
        ]:
            return None

        if record.addressline6 in [
            # splits
            "S33 0AB",
            "SK23 6BR",
            "SK22 3DU",  # LARKHILL TERRACE, NEW MILLS, HIGH PEAK
        ]:
            return None

        return super().address_record_to_dict(record)
