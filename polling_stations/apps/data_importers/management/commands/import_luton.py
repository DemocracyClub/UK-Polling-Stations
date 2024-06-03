from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "LUT"
    addresses_name = "2024-07-04/2024-06-07T10:26:05.054644/Democracy Club - Polling Districts (1).csv"
    stations_name = "2024-07-04/2024-06-07T10:26:05.054644/Democracy Club - Polling Stations (1).csv"
    elections = ["2024-07-04"]
    csv_encoding = "utf-16le"

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "100080141870",  # 169 DEWSBURY ROAD, LUTON
            "100080163617",  # 117 NEVILLE ROAD, LUTON
            "100080124758",  # 166 ALEXANDRA AVENUE, LUTON
            "10095334110",  # 654A DENBIGH ROAD, LUTON
        ]:
            return None

        if record.postcode in [
            # splits
            "LU1 3XD",
            # looks wrong
            "LU2 8PE",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        if record.stationcode in (
            "101",  # Billington Village Hall (CBF)
            "102",  # Eaton Bray Village Hall (CBF)
            "93",  # Heathfield Site (CBF)
            "94",  # Heathfield Site (CBF)
            "96",  # Kaisho Academy of Martial Arts Hall (CBF)
            "97",  # Kensworth Village Hall (CBF)
            "95",  # Lyons Community Centre (CBF)
            "98",  # Slip End Village Hall (CBF)
            "103",  # St Giles Church Hall (CBF)
            "99",  # Studham Village Hall (CBF)
            "100",  # Whipsnade Village Hall (CBF)
        ):
            return None
        return super().station_record_to_dict(record)
