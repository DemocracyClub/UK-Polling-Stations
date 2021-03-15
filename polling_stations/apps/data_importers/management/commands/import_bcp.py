from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "BPC"
    addresses_name = "2021-03-15T10:07:53.031696/BCP Democracy_Club__06May2021.tsv"
    stations_name = "2021-03-15T10:07:53.031696/BCP Democracy_Club__06May2021.tsv"
    elections = ["2021-05-06"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "100040790272",  # FLAT 5, HAZELDENE, 2 YORK ROAD, BROADSTONE
            "10094773056",  # 10B NAIRN ROAD, POOLE
            "10012226208",  # FLAT 2, PRIORY HOUSE, ATHELSTAN ROAD, BOURNEMOUTH
            "10012226209",  # FLAT 3, PRIORY HOUSE, ATHELSTAN ROAD, BOURNEMOUTH
            "10012226210",  # FLAT 4, PRIORY HOUSE, ATHELSTAN ROAD, BOURNEMOUTH
            "10024391215",  # APARTMENT B TUDOR HOUSE 1 WALPOLE ROAD, BOURNEMOUTH
        ]:
            return None

        if record.addressline6 in [
            "BH15 3FG",
            "BH10 6BA",
            "BH5 1FG",
            "BH1 1NF",
            "BH1 3EB",
            "BH7 6LL",
            "BH6 3NH",
            "BH6 3BJ",
            "BH10 5JF",
            "BH6 3LF",
            "BH12 4EB",
            "BH5 1DL",
            "BH14 0RD",
            "BH23 3JJ",
        ]:
            return None

        return super().address_record_to_dict(record)
