from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "TOF"
    addresses_name = "2024-07-04/2024-06-04T15:57:58.919976/Democracy Club Converted - 2024-05-30 noBOM.csv"
    stations_name = "2024-07-04/2024-06-04T15:57:58.919976/Democracy Club Converted - 2024-05-30 noBOM.csv"
    elections = ["2024-07-04"]

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "200002953910",  # PARK HOUSE FARM, GRAIG ROAD, UPPER CWMBRAN, CWMBRAN
            "10013477141",  # GELLI FAWR FARM, HENLLYS, CWMBRAN
        ]:
            return None

        if record.housepostcode.strip() in [
            # split
            "NP4 8LG",
            "NP4 7NW",
            "NP44 5AB",
            # suspect
            "NP4 8QW",
            "NP4 8QP",
            "NP4 6TX",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # The following stations have postcodes that don't match their postcode in addressbase:
        # They're only off by one letter so I've commented them out until the council responds

        # # 'GARNDIFFAITH MILLENNIUM HALL, TOP ROAD, GARNDIFFAITH, PONTYPOOL, TORFAEN, NP4 7LT' (id: 54)
        # if record.pollingvenueid == "54":
        #     record = record._replace(pollingstationpostcode="NP4 7LY")

        # # 'VICTORIA VILLAGE COMMUNITY HALL, CWMAVON ROAD, VICTORIA VILLAGE, ABERSYCHAN, TORFAEN, NP4 8PT' (id: 76)
        # if record.pollingvenueid == "76":
        #     record = record._replace(pollingstationpostcode="NP4 8PL")

        # # 'TRINITY METHODIST CHAPEL, HIGH STREET, ABERSYCHAN, PONTYPOOL, TORFAEN, NP4 7AE' (id: 6)
        # if record.pollingvenueid == "6":
        #     record = record._replace(pollingstationpostcode="NP4 7AZ")

        # # 'PONTNEWYNYDD EBENEZER CHAPEL HALL, CHAPEL ROAD, PONTNEWYNYDD, PONTYPOOL, TORFAEN, NP4 6QR' (id: 14)
        # if record.pollingvenueid == "14":
        #     record = record._replace(pollingstationpostcode="NP4 6QN")

        # # 'PONTYMOILE UNDENOMINATIONAL MISSION, ROCKHILL ROAD, PONTYMOILE, PONTYPOOL, TORFAEN, NP4 8AR' (id: 50)
        # if record.pollingvenueid == "50":
        #     record = record._replace(pollingstationpostcode="NP4 8AN")

        # # 'ST OSWALDS CHURCH, WERN ROAD, SEBASTOPOL, PONTYPOOL, TORFAEN, NP4 5DS' (id: 82)
        # if record.pollingvenueid == "82":
        #     record = record._replace(pollingstationpostcode="NP4 5DU")

        # # 'NURSERY NEW INN PRIMARY SCHOOL, ENTRANCE VIA GOLF ROAD, NEW INN, PONTYPOOL, TORFAEN, NP4 0PR' (id: 26)
        # if record.pollingvenueid == "26":
        #     record = record._replace(pollingstationpostcode="NP4 0NG")

        # # 'NEW INN COMMUNITY HALL, NEW ROAD, NEW INN, PONTYPOOL, TORFAEN, NP4 0PZ' (id: 85)
        # if record.pollingvenueid == "85":
        #     record = record._replace(pollingstationpostcode="NP4 0TN")

        # # 'GLASLYN COMMUNITY CENTRE, GLASLYN COURT, CROESYCEILIOG, CWMBRAN, TORFAEN, NP44 2JE' (id: 45)
        # if record.pollingvenueid == "45":
        #     record = record._replace(pollingstationpostcode="NP44 2JH")
        return super().station_record_to_dict(record)
