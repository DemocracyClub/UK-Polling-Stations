from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "WYR"
    addresses_name = (
        "2023-05-04/2023-03-21T14:04:15.276082/Democracy_Club__04May2023.tsv"
    )
    stations_name = (
        "2023-05-04/2023-03-21T14:04:15.276082/Democracy_Club__04May2023.tsv"
    )
    elections = ["2023-05-04"]
    csv_encoding = "windows-1252"
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10003527163",  # 3 GARNET CLOSE, THORNTON-CLEVELEYS
            "10024171572",  # WELL WOOD VIEW, STATION LANE, SCORTON, PRESTON
            "10093999437",  # PLEASANT VIEW, BLACKPOOL ROAD, POULTON-LE-FYLDE
            "10034085598",  # MANOR VALE, ST. MICHAELS ROAD, BILSBORROW, PRESTON
            "100012422216",  # MANOR HOUSE FARM, ST. MICHAELS ROAD, BILSBORROW, PRESTON
            "10034083802",  # FIELDVIEW, PINFOLD LANE, SOWERBY, PRESTON
        ]:
            return None

        if record.post_code in [
            "FY6 7GH",  # CHURCH COURT, POULTON-LE-FYLDE
            "FY7 6FJ",  # SPINNAKER CLOSE, FLEETWOOD
            "PR3 1TS",  # FOREST VIEW PLACE, SCORTON
            "PR3 1ZW",  # CEDAR WOOD CLOSE, BOWGREAVE, PRESTON
        ]:
            return None

        return super().address_record_to_dict(record)
