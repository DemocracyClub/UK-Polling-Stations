from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "NOW"
    addresses_name = "2022-05-05/2022-04-13T13:59:25.402641/Democracy Club  - Polling districts export.csv"
    stations_name = "2022-05-05/2022-04-13T13:59:25.402641/Democracy Club  - Polling stations export.csv"
    elections = ["2022-05-05"]

    def station_record_to_dict(self, record):
        # PILLING PARK COMMUNITY CENTRE, 23 PILLING PARK ROAD, NORWICH
        if record.stationcode == "10CR1":
            record = record._replace(xordinate="625225", yordinate="308971")
        # THE NORWICH HOTEL, 116 THORPE ROAD, NORWICH
        elif record.stationcode == "43TH3":
            record = record._replace(xordinate="624318", yordinate="308290")
        # ST MATTHEW'S CHURCH, TELEGRAPH LANE WEST, NORWICH
        elif record.stationcode == "44TH4":
            record = record._replace(xordinate="624342", yordinate="308878")
        # CHANTRY HALL, THE CHANTRY, CHANTRY ROAD, NORWICH
        elif record.stationcode == "25MA3":
            record = record._replace(xordinate="622805", yordinate="308252")
        # TRINITY UNITED REFORMED CHURCH HALL, 1 UNTHANK ROAD, NORWICH
        elif record.stationcode == "34NE3":
            record = record._replace(xordinate="622293", yordinate="308473")
        # DOURO PLACE CHAPEL, DOURO PLACE, DEREHAM ROAD, NORWICH
        elif record.stationcode == "36NE5":
            record = record._replace(xordinate="622053", yordinate="308857")
        # CAMBRIDGE STREET HALL, 54 CAMBRIDGE STREET, NORWICH
        elif record.stationcode == "46TO2":
            record = record._replace(xordinate="622138", yordinate="307955")
        # RECREATION ROAD SPORTS CENTRE, RECREATION ROAD, NORWICH
        elif record.stationcode == "33NE2":
            record = record._replace(xordinate="621293", yordinate="308399")
        # WEST EARLHAM COMMUNITY CENTRE, 10 WILBERFORCE ROAD, NORWICH
        elif record.stationcode == "54UN5":
            record = record._replace(xordinate="619048", yordinate="308702")
        # ST MARY'S CHURCH HALL, HUTCHINSON ROAD, NORWICH
        elif record.stationcode == "50UN1":
            record = record._replace(xordinate="619515", yordinate="308822")
        # ST ANNE'S CHURCH HALL, 150-160 COLMAN ROAD, NORWICH
        elif record.stationcode == "52UN3":
            record = record._replace(xordinate="620695", yordinate="308121")
        elif record.stationcode in [
            "26MA4",  # CASTLE QUARTER, CASTLE QUARTER, LEVEL 4, TIMBERHILL ENTRANCE, TIMBERHILL, NORWICH
            "14CR5",  # NORWICH PREMIER JUDO CLUB (HEATHGATE COMMUNITY CENTRE), HEATHGATE COMMUNITY CENTRE, 6 HEATHGATE, NORWICH
            "28MX1",  # ST LUKE'S CHURCH CENTRE, 61 AYLSHAM ROAD, NORWICH
            "19LA1",  # TUCKSWOOD LIBRARY, ROBIN HOOD ROAD, NORWICH
        ]:
            record = record._replace(xordinate="", yordinate="")
        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "100091562008",  # 10 SPROWSTON ROAD, NORWICH
            "10090481878",  # 141B UNTHANK ROAD, NORWICH
            "100090915857",  # 9 OAK STREET, NORWICH
            "100090915856",  # 7 OAK STREET, NORWICH
            "100090915855",  # 5 OAK STREET, NORWICH
            "100090915854",  # 3 OAK STREET, NORWICH
        ]:
            return None

        return super().address_record_to_dict(record)
