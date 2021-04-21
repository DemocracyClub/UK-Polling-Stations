from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "NWP"
    addresses_name = "2021-04-14T15:41:04.216488/Democracy_Club__06May2021.tsv"
    stations_name = "2021-04-14T15:41:04.216488/Democracy_Club__06May2021.tsv"
    elections = ["2021-05-06"]
    csv_delimiter = "\t"
    csv_encoding = "latin-1"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10002155274",  # ORCHARD FARM, ST. BRIDES WENTLOOGE, NEWPORT
            "10002155651",  # BLUEBELL COTTAGE, ST. BRIDES WENTLOOGE, NEWPORT
            "10002147773",  # WERN FARM, RHIWDERIN, NEWPORT
            "100100654811",  # 196 CARDIFF ROAD, NEWPORT
            "100100654809",  # 194 CARDIFF ROAD, NEWPORT
            "100100654807",  # 192 CARDIFF ROAD, NEWPORT
            "100100654805",  # 190 CARDIFF ROAD, NEWPORT
            "100100654804",  # 188 CARDIFF ROAD, NEWPORT
            "10090277427",  # FLAT 3 25 CARDIFF ROAD, NEWPORT
            "10090277428",  # FLAT 5 25 CARDIFF ROAD, NEWPORT
            "10090277426",  # FLAT 2 25 CARDIFF ROAD, NEWPORT
            "100100677933",  # 512 MONNOW WAY, BETTWS, NEWPORT
            "10093295441",  # TY TERNION, LODGE ROAD, CAERLEON, NEWPORT
            "10090277366",  # 5C TURNER STREET, NEWPORT
            "10010553788",  # 39 REMBRANDT WAY, NEWPORT
            "10002154176",  # 124B CHEPSTOW ROAD, NEWPORT
            "100101046500",  # 124A CHEPSTOW ROAD, NEWPORT
            "10090275166",  # 8 MAPLE CLOSE, NEWPORT
            "10002153590",  # RED ROBIN HOUSE, LLANDEVAUD, NEWPORT
            "100100668792",  # YEW TREE COTTAGE, HENDREW LANE, LLANDEVAUD, NEWPORT
            "10002153797",  # MEADOW BROOK, PENHOW, CALDICOT
            "200001705281",  # GREENACRES, PENHOW, CALDICOT
            "10009646166",  # THE LAURELS, GREENACRES, PENHOW, CALDICOT
            "200001652454",  # LITTLE CAERLICKEN, CAERLICYN LANE, LANGSTONE, NEWPORT
            "200002951720",  # ABBEYFIELD SOCIETY, ELEANOR HODSON HOUSE, PILLMAWR ROAD, CAERLEON, NEWPORT
            "10014125673",  # MANAGERS ACCOMMODATION THE WINDSOR CLUB 154-156 CONWAY ROAD, NEWPORT
        ]:
            return None

        if record.post_code in ["NP19 9BX", "NP10 8AT"]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):

        # East Hub 282 Ringland Circle Newport
        if record.polling_place_id == "11949":
            record = record._replace(polling_place_postcode="NP19 9PS")

        # Correction from council addresses going to The Dodger, Chepstow Road now going to Community House, Eton Road
        if record.polling_place_id == "12187":
            record = record._replace(
                polling_place_name="Community House Eton Road",
                polling_place_address_1="Eton Road",
                polling_place_address_2="Newport",
                polling_place_address_3="",
                polling_place_address_4="",
                polling_place_postcode="NP19 0BL",
                polling_place_easting="0",
                polling_place_northing="0",
                polling_place_uprn="",
            )

        return super().station_record_to_dict(record)
