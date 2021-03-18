from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "TRF"
    addresses_name = "2021-03-17T16:41:00.619202/Democracy_Club__06May2021.CSV"
    stations_name = "2021-03-17T16:41:00.619202/Democracy_Club__06May2021.CSV"
    elections = ["2021-05-06"]
    csv_delimiter = ","

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10070444818",  # FOUR OAKS CARE HOME, 28 WOOD LANE, PARTINGTON, MANCHESTER
            "100011622567",  # 52B ARDERNE ROAD, TIMPERLEY, ALTRINCHAM
            "10070457195",  # 86 HEYES LANE, TIMPERLEY, ALTRINCHAM
            "10070457196",  # 4A BROOMFIELD LANE, HALE
            "200000333947",  # 161 STOCKPORT ROAD, TIMPERLEY, ALTRINCHAM
            "100011646326",  # 5 SOUTH CROSTON STREET, MANCHESTER
            "100011640670",  # 3 SOUTH CROSTON STREET, MANCHESTER
            "10070457194",  # 238 AYRES ROAD, MANCHESTER
            "100012699156",  # DOG BEAUTY, 96 PARK ROAD, TIMPERLEY, ALTRINCHAM
            "10070408519",  # 7 SOUTH CROSTON STREET, MANCHESTER
            "10070405338",  # 183A CROSS STREET, SALE
            "100011637164",  # RAILWAY TAVERN, IRLAM ROAD, URMSTON, MANCHESTER
            "100011632467",  # ST ANTONYS ROMAN CATHOLIC CHURCH ELEVENTH STREET, TRAFFORD PARK
            "100012489906",  # VALE LODGE, GRANGE ROAD, BOWDON, ALTRINCHAM
            "100011679026",  # 17 WOOD LANE, PARTINGTON, MANCHESTER
            "100011693362",  # 300 MANOR AVENUE, SALE
        ]:
            return None

        if record.addressline6 in [
            "M41 9JA",
            "M33 5BA",
            "WA14 4RJ",
            "WA14 2AL",
            "M33 2BT",
            "M41 6JU",
            "M33 6NH",
        ]:
            return None

        return super().address_record_to_dict(record)
