from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "RUN"
    addresses_name = (
        "2024-07-04/2024-05-29T09:00:57.033219/Democracy_Club__04July2024.tsv"
    )
    stations_name = (
        "2024-07-04/2024-05-29T09:00:57.033219/Democracy_Club__04July2024.tsv"
    )
    elections = ["2024-07-04"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10092963299",  # FLAT AT 79 STATION ROAD, ADDLESTONE
            "10095815752",  # FLAT 50, AVIATOR HOUSE, 227 STATION ROAD, ADDLESTONE
            "10095815848",  # FLAT 136, AVIATOR HOUSE, 227 STATION ROAD, ADDLESTONE
            "10095815743",  # FLAT 32, AVIATOR HOUSE, 227 STATION ROAD, ADDLESTONE
            "200004029979",  # LODGE, ST. GEORGES COLLEGE, WEYBRIDGE ROAD, ADDLESTONE
            "100062604551",  # ST. GEORGES COLLEGE, WEYBRIDGE ROAD, ADDLESTONE
            "100062600234",  # RUSHAM COTTAGE, PRUNE HILL, ENGLEFIELD GREEN, EGHAM
            "10092962917",  # JAKES FARM, BROX LANE, OTTERSHAW, CHERTSEY
            "10092961689",  # GEORGE ELIOT HOUSE, HARVEST ROAD, ENGLEFIELD GREEN, EGHAM
        ]:
            return None
        if record.addressline6 in [
            # splits
            "KT16 8QD",
            "KT16 8AG",
            "KT15 2DB",
            "KT16 0AB",  # 10 WATERY LANE, CHERTSEY
        ]:
            return None

        return super().address_record_to_dict(record)
