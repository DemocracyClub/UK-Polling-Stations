from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "CHL"
    addresses_name = "2021-03-23T14:10:30.146530/Democracy_Club__06May2021.tsv"
    stations_name = "2021-03-23T14:10:30.146530/Democracy_Club__06May2021.tsv"
    elections = ["2021-05-06"]
    csv_delimiter = "\t"
    csv_encoding = "windows-1252"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10093929304",  # 85 BROOMFIELD ROAD, CHELMSFORD
            "100091234139",  # 1 BANKSIDE, NEW STREET, CHELMSFORD
            "100091430409",  # BARNES MILL HOUSE, MILL VUE ROAD, CHELMSFORD
            "100090390510",  # HONEYSTONE, SOUTHEND ROAD, HOWE GREEN, CHELMSFORD
            "100090390509",  # NEW BUNGALOW, TURKEY FARM, WINDSOR TRADING ESTATE, WINDSOR ROAD, DOWNHAM, BILLERICAY
            "200004627211",  # FLAT 30 RAINSFORD ROAD, CHELMSFORD
            "10013265486",  # BASSMENT NIGHTCLUB, 16-18 WELLS STREET, CHELMSFORD
            "10093928503",  # 67 BROOMFIELD ROAD, CHELMSFORD
            "200004630041",  # 1 LIBERTY WAY, RUNWELL, WICKFORD
            "100091236477",  # KENILWORTH, WOODHILL ROAD, DANBURY, CHELMSFORD
            "10093928503",  # HONEYSTONE, SOUTHEND ROAD, HOWE GREEN, CHELMSFORD
        ]:
            return None

        if record.addressline6 in [
            "CM3 5XW",
            "CM4 9JL",
            "CM1 3FH",
            "CM1 2HL",
            "CM2 6JL",
            "CM1 1LA",
        ]:
            return None

        return super().address_record_to_dict(record)
