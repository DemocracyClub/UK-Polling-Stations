from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "NLN"
    addresses_name = (
        "2021-04-08T14:14:26.248859/polling_station_export-North Lincolnshire.csv"
    )
    stations_name = (
        "2021-04-08T14:14:26.248859/polling_station_export-North Lincolnshire.csv"
    )
    elections = ["2021-05-06"]
    csv_delimiter = ","

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "200000888660",  # INGLENOOK, STATION ROAD, SCAWBY, BRIGG
            "200000890811",  # WAVERNEY, SUSWORTH, SCUNTHORPE
            "200000885882",  # 268A ASHBY HIGH STREET, SCUNTHORPE
            "10002633740",  # FIRST FLOOR 260 ASHBY HIGH STREET, SCUNTHORPE
            "10024384054",  # FLAT 1, 258 ASHBY HIGH STREET, SCUNTHORPE
            "10002632625",  # FLAT 220 ASHBY HIGH STREET, SCUNTHORPE
            "10002632632",  # FLAT THE MALT SHOVEL 219 ASHBY HIGH STREET, SCUNTHORPE
            "100050194026",  # 213A ASHBY HIGH STREET, SCUNTHORPE
            "100051968332",  # 211B ASHBY HIGH STREET, SCUNTHORPE
            "100051967026",  # 68A MARY STREET, SCUNTHORPE
            "10095555490",  # FLAT 3 175 HIGH STREET, SCUNTHORPE
            "10013438569",  # FLAT PIG AND WHISTLE WINTERTON ROAD, SCUNTHORPE
            "10091168760",  # PART A3 AUCTION ROOM AND PREMISES WINTERTON ROAD, SCUNTHORPE
            "200000893947",  # FLAT, 265 FRODINGHAM ROAD, SCUNTHORPE
            "100051966763",  # 147A FRODINGHAM ROAD, SCUNTHORPE
            "100051966807",  # FLAT, 145 FRODINGHAM ROAD, SCUNTHORPE
            "100050226727",  # 77 WHARF ROAD, CROWLE, SCUNTHORPE
        ]:
            return None

        if record.housepostcode in [
            "DN16 2PG",
            "DN17 1PT",
            "DN17 1SB",
            "DN15 7JH",
            "DN20 0SD",
            "DN17 4EJ",
            "DN15 8XL",
            "DN18 5BF",
            "DN15 6TL",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # Wootton Village Hall Swallow Lane Wootton DN39 6SY
        if (
            record.pollingstationnumber == "114"
            and record.pollingstationpostcode == "DN39 6SY"
        ):
            record = record._replace(pollingstationpostcode="")

        return super().station_record_to_dict(record)
