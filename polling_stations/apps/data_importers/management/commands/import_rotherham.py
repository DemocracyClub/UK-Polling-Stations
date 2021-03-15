from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "ROT"
    addresses_name = "2021-03-15T11:29:31.675704/Democracy_Club__06May2021.tsv"
    stations_name = "2021-03-15T11:29:31.675704/Democracy_Club__06May2021.tsv"
    elections = ["2021-05-06"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10032994571",  # MOBILE HOME 1 MANSFIELD ROAD, ASTON, ROTHERHAM
            "10091630508",  # 11 SCHOLEY ROAD, WICKERSLEY, ROTHERHAM
            "100050829576",  # 9 DALE HILL ROAD, MALTBY, ROTHERHAM
            "10023210795",  # 15 SCHOLEY ROAD, WICKERSLEY, ROTHERHAM
            "100050867055",  # 9 SCHOLEY ROAD, WICKERSLEY, ROTHERHAM
            "100050867059",  # 13 SCHOLEY ROAD, WICKERSLEY, ROTHERHAM
            "100050867053",  # CROFT BANK, CHAPEL HILL, WHISTON, ROTHERHAM
            "100050867057",  # ELDERTREE LODGE, SHAWS FARM, ELDERTREE ROAD, THORPE HESLEY, ROTHERHAM
            "200000580837",  # LIVING ACCOMODATION SAXON HOTEL STATION ROAD, KIVETON PARK, ROTHERHAM
            "10023209193",  # 12 MAIN STREET, AUGHTON, SHEFFIELD
        ]:
            return None

        if record.addressline6 in [
            "S65 1PQ",
            "S64 5UU",
            "S63 6HF",
            "S64 8PG",
            "S64 8DQ",
            "S64 8QA",
            "S26 4XB",
            "S60 4FB",
            "S26 2DA",
        ]:
            return None

        return super().address_record_to_dict(record)
