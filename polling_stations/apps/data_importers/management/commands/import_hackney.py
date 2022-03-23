from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "HCK"
    addresses_name = "2022-05-05/2022-03-23T17:30:06.543100/Democracy_Club__05May2022-HackneyCouncilPollingStations.CSV"
    stations_name = "2022-05-05/2022-03-23T17:30:06.543100/Democracy_Club__05May2022-HackneyCouncilPollingStations.CSV"
    elections = ["2022-05-05"]

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "100021050062",  # BASEMENT AND GROUND FLOOR 100 LOWER CLAPTON ROAD, HACKNEY, LONDON
            "10008340028",  # FLAT E, 112 KINGSLAND ROAD, LONDON
            "10008300957",  # 85 CASTLEWOOD ROAD, HACKNEY, LONDON
            "200001073528",  # POTTERY HOUSE, ELRINGTON ROAD, LONDON
            "10008233474",
            "10008342758",
            "10008354539",
            "100021076655",
            "10008340573",
            "100021032861",
        ]:
            return None

        if record.addressline6 in [
            "N1 6RH",
            "E20 3AZ",
            "E8 2NS",
            "N4 2ZB",
            "N4 2LD",
            "N4 2WQ",
            "E2 8FZ",
            "N16 0SD",
            "E5 9AP",
            "N16 0RT",
            "EC2A 2FJ",
        ]:
            return None

        return super().address_record_to_dict(record)
