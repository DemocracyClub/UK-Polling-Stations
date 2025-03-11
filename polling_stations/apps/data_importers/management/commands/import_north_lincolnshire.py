from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "NLN"
    addresses_name = "2025-05-01/2025-03-11T17:08:37.404782/Polling Stations-North Lincolnshire Council.csv"
    stations_name = "2025-05-01/2025-03-11T17:08:37.404782/Polling Stations-North Lincolnshire Council.csv"
    elections = ["2025-05-01"]

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")
        if (
            uprn
            in [
                "200000888905",  # LITTLE GRANGE, FERRIBY ROAD, BARTON-UPON-HUMBER
                "10095555254",  # THE BARN, LITTLE GRANGE, FERRIBY ROAD, BARTON-UPON-HUMBER
                "10095555254",  # THE BARN, LITTLE GRANGE, FERRIBY ROAD, BARTON-UPON-HUMBER
                "100050213509",  # REAR OF 121, MARY STREET, SCUNTHORPE
                "100051967026",  # 68A MARY STREET, SCUNTHORPE
                "200000890811",  # WAVERNEY, SUSWORTH, SCUNTHORPE
                "200000889029",  # MASLAM HALL, BRIGG ROAD, BARTON-UPON-HUMBER
                "200000890331",  # WILFREDS TOP BUNGALOW B1206 BETWEEN NORTHWOLD FARM AND BRIGG ROAD, BONBY
                "10002635448",  # FLAT ASHBY LODGE MORTAL ASH HILL, SCUNTHORPE
                "200000876730",  # SNOW SEWER BUNGALOW, PARK DRAIN, WESTWOODSIDE, DONCASTER
            ]
        ):
            return None

        if record.housepostcode in [
            # split
            "DN20 0SD",
            "DN17 1SB",
            "DN15 8XL",
            "DN15 7JH",
            # suspect,
            "DN18 5BF",
            "DN16 2RX",
            "DN16 2SE",
            "DN8 5SW",
            "DN8 5SX",
            "DN15 6LN",
        ]:
            return None
        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # Add missing postcode for Function Room, Haven Inn, Ferry Road, Barrow Haven
        if record.pollingstationnumber == "83":
            record = record._replace(pollingstationpostcode="DN19 7EX")

        return super().station_record_to_dict(record)
