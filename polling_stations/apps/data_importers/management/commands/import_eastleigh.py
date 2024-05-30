from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "EAT"
    addresses_name = (
        "2024-07-04/2024-05-30T17:35:45.611401/Democracy_Club__04July2024.tsv"
    )
    stations_name = (
        "2024-07-04/2024-05-30T17:35:45.611401/Democracy_Club__04July2024.tsv"
    )
    elections = ["2024-07-04"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "200002902856",  # FLAT, 2 WINCHESTER ROAD, CHANDLER'S FORD, EASTLEIGH
            "10091134664",  # CHERRYWOOD, LOWFORD HILL, BURSLEDON, SOUTHAMPTON
            "10091134663",  # LARCHWOOD, LOWFORD HILL, BURSLEDON, SOUTHAMPTON
            "10091134662",  # ASHWOOD, LOWFORD HILL, BURSLEDON, SOUTHAMPTON
            "10091134661",  # SPINDLEWOOD, LOWFORD HILL, BURSLEDON, SOUTHAMPTON
            "10009640001",  # OAK COTTAGE, ALLINGTON LANE, FAIR OAK, EASTLEIGH
            "10094386469",  # THE HOUND WB02, SATCHELL LANE, HAMBLE, SOUTHAMPTON
            "100060324530",  # POND FARM, MORTIMERS LANE, UPHAM, SOUTHAMPTON
        ]:
            return None

        if record.addressline6 in [
            # split
            "SO30 0DF",
            "SO31 8AF",
        ]:
            return None

        return super().address_record_to_dict(record)
