from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "SGC"
    addresses_name = "2021-04-09T13:58:02.959505/Democracy_Club__06May2021.tsv"
    stations_name = "2021-04-09T13:58:02.959505/Democracy_Club__06May2021.tsv"
    elections = ["2021-05-06"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "684376",  # THE WIGEON, ELBERTON ROAD, ELBERTON, OLVESTON, BRISTOL
            "641732",  # ORCHARD HOUSE, PARK ROAD, LEYHILL, WOTTON-UNDER-EDGE
            "687668",  # CHERRY COTTAGE, BRISTOL ROAD, IRON ACTON, BRISTOL
            "678521",  # 13A SHRUBBERY COURT, NELSON ROAD, BRISTOL
            "604995",  # FIFTEEN ACRES FARM, BEACH, BITTON, BRISTOL
            "684790",  # THE PADDOCK, DODINGTON LANE, DODINGTON, CHIPPING SODBURY, BRISTOL
            "606757",  # BATH LODGE, DODINGTON ASH, CHIPPING SODBURY, BRISTOL
        ]:
            return None

        if record.addressline6 in [
            "GL12 8HT",
            "BS30 5TP",
            "BS37 8QH",
            "GL12 8PX",
            "BS32 4AH",
            "BA1 8HD",
            "BS37 7BN",
            "BS16 4RP",
            "BS16 1UY",
            "BS15 3HW",
            "BS15 8EG",
            "BS15 8GA",
            "BS16 1RR",
            "BS37 7BZ",
            "BS16 4LZ",
            "BS35 1LG",
            "BS35 1BP",
            "BS15 3HP",
            "BS37 6DF",
            "BS35 4JA",
        ]:
            return None

        return super().address_record_to_dict(record)
