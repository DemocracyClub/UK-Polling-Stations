from data_importers.management.commands import BaseHalaroseCsvImporter


def station_update(record):
    # Council station change from:
    # Main Street, Redbourne, Gainsborough, Lincolnshire, DN21 4QN
    # to:
    # St Andrews Church, 2 School Lane, Redbourne, Lincolnshire, DN21 4QN

    if record.pollingstationnumber == "109":
        record = record._replace(
            pollingstationname="St Andrews Church",
            pollingstationnumber="109",
            pollingstationaddress_1="2 School Lane",
            pollingstationaddress_2="Redbourne",
            pollingstationaddress_3="Gainsborough",
            pollingstationaddress_4="Lincolnshire",
            pollingstationaddress_5="",
            pollingstationpostcode="DN21 4QN",
        )
    return record


class Command(BaseHalaroseCsvImporter):
    council_id = "NLN"
    addresses_name = "2023-05-04/2023-04-12T16:20:54.855801/Eros_SQL_Output002.csv"
    stations_name = "2023-05-04/2023-04-12T16:20:54.855801/Eros_SQL_Output002.csv"
    elections = ["2023-05-04"]

    def address_record_to_dict(self, record):
        record = station_update(record)

        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "100051967026",  # 68A MARY STREET, SCUNTHORPE
            "10095555490",  # FLAT 3 175 HIGH STREET, SCUNTHORPE
            "200000893947",  # FLAT, 265 FRODINGHAM ROAD, SCUNTHORPE
            "100051966763",  # 147A FRODINGHAM ROAD, SCUNTHORPE
            "100051966807",  # FLAT, 145 FRODINGHAM ROAD, SCUNTHORPE
            "100050226727",  # 77 WHARF ROAD, CROWLE, SCUNTHORPE
        ]:
            return None

        if record.housepostcode in [
            # split
            "DN17 1SB",
            "DN15 8XL",
            "DN17 4EJ",
            "DN20 0SD",
            "DN15 7JH",
            "DN21 4JF",
            # look wrong
            "DN16 2RX",
            "DN16 2SE",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        record = station_update(record)

        return super().station_record_to_dict(record)
