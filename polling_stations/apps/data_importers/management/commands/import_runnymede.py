from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "RUN"
    addresses_name = (
        "2023-05-04/2023-03-02T14:04:03.113510/Democracy_Club__04May2023.tsv"
    )
    stations_name = (
        "2023-05-04/2023-03-02T14:04:03.113510/Democracy_Club__04May2023.tsv"
    )
    elections = ["2023-05-04"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10091662635",  # 3 CLIFTON GRANGE, BLACKPOOL ROAD, CLIFTON, PRESTON
            "10092963299",  # FLAT AT 79 STATION ROAD, ADDLESTONE
            "10095815752",  # FLAT 50, AVIATOR HOUSE, 227 STATION ROAD, ADDLESTONE
            "10095815848",  # FLAT 136, AVIATOR HOUSE, 227 STATION ROAD, ADDLESTONE
            "10095815743",  # FLAT 32, AVIATOR HOUSE, 227 STATION ROAD, ADDLESTONE
            "200004029979",  # LODGE, ST. GEORGES COLLEGE, WEYBRIDGE ROAD, ADDLESTONE
            "100062604551",  # ST. GEORGES COLLEGE, WEYBRIDGE ROAD, ADDLESTONE
        ]:
            return None
        if record.addressline6 in [
            # splits
            "KT16 8QD",
            "KT16 8AG",
            "KT15 2US",
            "KT15 2DB",
            "KT16 0AB",  # 10 WATERY LANE, CHERTSEY
        ]:
            return None

        return super().address_record_to_dict(record)
