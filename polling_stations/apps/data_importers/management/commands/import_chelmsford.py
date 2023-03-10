from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "CHL"
    addresses_name = (
        "2023-05-04/2023-03-10T11:52:49.383052/Democracy_Club__04May2023.tsv"
    )
    stations_name = (
        "2023-05-04/2023-03-10T11:52:49.383052/Democracy_Club__04May2023.tsv"
    )
    elections = ["2023-05-04"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "100091234139",  # 1 BANKSIDE, NEW STREET, CHELMSFORD
            "100091430409",  # BARNES MILL HOUSE, MILL VUE ROAD, CHELMSFORD
            "10093928503",  # 67 BROOMFIELD ROAD, CHELMSFORD
            "200004630041",  # 1 LIBERTY WAY, RUNWELL, WICKFORD
            "10093928503",  # HONEYSTONE, SOUTHEND ROAD, HOWE GREEN, CHELMSFORD
            "10094901647",  # 1 MERCHANT STREET, SOUTH WOODHAM FERRERS, CHELMSFORD
            "200004627211",  # BARNES MILL HOUSE, MILL VUE ROAD, CHELMSFORD
            "10093928515",  # CARAVAN 2 AT OAKVALE DOMSEY LANE, LITTLE WALTHAM, CHELMSFORD
        ]:
            return None

        if record.addressline6 in [
            # split
            "CM1 7AR",
            "CM4 9JL",
            "CM3 1ER",
        ]:
            return None

        return super().address_record_to_dict(record)
