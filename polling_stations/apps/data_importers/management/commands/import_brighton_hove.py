from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "BNH"
    addresses_name = "2024-07-04/2024-05-28T14:03:04.608768/Brighton & Hove Democracy_Club__04July2024.tsv"
    stations_name = "2024-07-04/2024-05-28T14:03:04.608768/Brighton & Hove Democracy_Club__04July2024.tsv"
    elections = ["2024-07-04"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "22031382",  # COURT FARM HOUSE COURT FARM DEVIL'S DYKE ROAD, HOVE
            "22175494",  # THE LODGE, BRIGHTON RACE COURSE, FRESHFIELD ROAD, BRIGHTON
            "22272586",  # 1 GREEN MEWS, 53 HOGARTH ROAD, HOVE
            "22272587",  # 2 GREEN MEWS, 53 HOGARTH ROAD, HOVE
            "22272588",  # 3 GREEN MEWS, 53 HOGARTH ROAD, HOVE
            "22279648",  # 184C PORTLAND ROAD, HOVE
            "22057837",  # 260 LONDON ROAD, PRESTON, BRIGHTON
            "22057280",  # 90 PEACOCK LANE, BRIGHTON
        ]:
            return None

        if record.addressline6 in [
            # split
            "BN2 9PA",
            "BN2 7AB",
            "BN1 8NF",
            "BN1 3AE",
            # suspect
            "BN4 12PL",  # MILE OAK ROAD, PORTSLADE, BRIGHTON
        ]:
            return None

        return super().address_record_to_dict(record)
