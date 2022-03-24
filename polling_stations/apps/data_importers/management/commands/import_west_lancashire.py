from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "WLA"
    addresses_name = (
        "2022-05-05/2022-03-24T16:56:09.201434/Democracy_Club__05May2022.tsv"
    )
    stations_name = (
        "2022-05-05/2022-03-24T16:56:09.201434/Democracy_Club__05May2022.tsv"
    )
    elections = ["2022-05-05"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10012357871",  # WILLOW BARN, GREEN LANE, TARLETON, PRESTON
            "10012353358",  # 24 SOUTHPORT ROAD, SCARISBRICK, SOUTHPORT
            "10012348052",  # GREEN LANE FARM, GREEN LANE, TARLETON, PRESTON
        ]:
            return None

        if record.addressline6 in [
            "L40 5BE",
            "L40 8JB",
            "L40 9QL",
            "WN8 8LL",
            "WN8 6SH",
            "WN8 7XA",
            "WN8 0BY",
        ]:
            return None

        return super().address_record_to_dict(record)
