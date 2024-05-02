from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "EPP"
    addresses_name = (
        "2024-05-02/2024-02-20T15:33:21.896325/Democracy_Club__02May2024.tsv"
    )
    stations_name = (
        "2024-05-02/2024-02-20T15:33:21.896325/Democracy_Club__02May2024.tsv"
    )
    elections = ["2024-05-02"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10012157511",  # WALLED GARDEN HOUSE, EPPING
            "10012157510",  # TIMBER LODGE, EPPING
            "100091477396",  # SCHOOL HOUSE, KING HAROLD SCHOOL, BROOMSTICK HALL ROAD, WALTHAM ABBEY
            "100091249452",  # SHONKS FARM, MILL STREET, HARLOW
            "100091251326",  # THE PANTILES, DUNMOW ROAD, FYFIELD, ONGAR
            "100091251152",  # THATCHED COTTAGE, BIRDS GREEN, WILLINGALE, ONGAR
            "10022857710",  # BLUNTS FARMHOUSE COOPERSALE LANE, THEYDON BOIS, EPPING
            "100091247388",  # BROOKSIDE, GRAVEL LANE, CHIGWELL
            "10022857825",  # CARAVAN 2 MOSS NURSERY SEDGE GREEN, ROYDON, HARLOW
            "200002755166",  # GARDEN COTTAGE, NURSERY ROAD, LOUGHTON
        ]:
            return None

        if record.addressline6 in [
            # splits
            "CM16 6JA",
            # suspect
            "CM5 0HP",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        rec = super().station_record_to_dict(record)
        # WCIVF bug report:
        # Removes map for: High Beach Village Hall, Avey Lane, High Beach, Loughton
        if rec["internal_council_id"] == "3468":
            rec["location"] = None

        return rec
