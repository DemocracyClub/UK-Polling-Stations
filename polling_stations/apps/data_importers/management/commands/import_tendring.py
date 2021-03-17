from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "TEN"
    addresses_name = "2021-03-16T13:49:32.237046/Democracy_Club__06May2021.tsv"
    stations_name = "2021-03-16T13:49:32.237046/Democracy_Club__06May2021.tsv"
    elections = ["2021-05-06"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "100091463517",  # 9 HEDGE END, WALTON ON THE NAZE
            "100091463343",  # 582 MAIN ROAD, HARWICH
            "100091269055",  # HEALTH & HAPPINESS, 558-560 MAIN ROAD, HARWICH
            "100090634963",  # GREYFRIARS, 2 BEACH ROAD, CLACTON-ON-SEA
            "100090602739",  # 18 ORWELL ROAD, CLACTON-ON-SEA
            "100091461472",  # 302 HIGH STREET, HARWICH
            "100090602737",  # 66 DULWICH ROAD, HOLLAND-ON-SEA, CLACTON-ON-SEA
            "10090658325",  # 64 DULWICH ROAD, HOLLAND-ON-SEA, CLACTON-ON-SEA
            "100090635156",  # FOOTS FARM RIDING CENTRE, THORPE ROAD, CLACTON-ON-SEA
            "100091273215",  # RIDGEMONT HOUSE LOW ROAD, DOVERCOURT
            "10007941736",  # SANS ETAGE, PLOUGH ROAD, GREAT BENTLEY, COLCHESTER
        ]:
            return None

        if record.addressline6 in ["CO16 8GU", "CO16 9R"]:
            return None

        return super().address_record_to_dict(record)
