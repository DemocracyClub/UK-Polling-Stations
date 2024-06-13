from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "NEL"
    addresses_name = "2024-07-04/2024-06-13T12:53:46.360961/Eros_SQL_Output002.csv"
    stations_name = "2024-07-04/2024-06-13T12:53:46.360961/Eros_SQL_Output002.csv"
    elections = ["2024-07-04"]

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "10090078903",  # FLAT, 247 GRIMSBY ROAD, CLEETHORPES
            "10090086605",  # THE ROOST, DIANA PRINCESS OF WALES HOSPITAL, SCARTHO ROAD, GRIMSBY
            "10090078890",  # FLAT 3, 50 RUTLAND STREET, GRIMSBY
            "10090078888",  # FLAT 1, 50 RUTLAND STREET, GRIMSBY
            "10090078889",  # FLAT 2, 50 RUTLAND STREET, GRIMSBY
            "10090078891",  # FLAT 4, 50 RUTLAND STREET, GRIMSBY
            "11023550",  # 38 BRAMHALL STREET, CLEETHORPES
            "11088787",  # 4 WALTHAM HOUSE FARM COTTAGE, LOUTH ROAD, NEW WALTHAM, GRIMSBY
            "11088786",  # WALTHAM HOUSE FARM COTTAGE 3 LOUTH ROAD, WALTHAM
        ]:
            return None

        if record.housepostcode in [
            "DN35 0RA",  # split
        ]:
            return None
        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # The following stations postcodes didn't match their postcode in addressbase
        # Because they're off by only one letter, I'm commmenting them out pending council response.

        # # CLEETHORPES LIBRARY, ALEXANDRA ROAD, CLEETHORPES, DN35 8LG (id: 17)
        # if record.pollingvenueid == "17":
        #     record = record._replace(pollingstationpostcode="DN35 8LQ")

        # # WENDOVER HALL, CHURCH LANE, HUMBERSTON, DN36 4HZ (id: 148)
        # if record.pollingvenueid == "148":
        #     record = record._replace(pollingstationpostcode="DN36 4HX")

        # # ALL SAINTS CHURCH HALL, HIGH STREET, WALTHAM, DN37 0PN (id: 80)
        # if record.pollingvenueid == "80":
        #     record = record._replace(pollingstationpostcode="DN37 0PL")

        # # HABROUGH VILLAGE HALL, STATION ROAD, HABROUGH, DN40 3BD (id: 48)
        # if record.pollingvenueid == "48":
        #     record = record._replace(pollingstationpostcode="DN40 3BQ")

        # # STALLINGBOROUGH VILLAGE HALL, STATION ROAD, STALLINGBOROUGH, DN41 8AJ (id: 49)
        # if record.pollingvenueid == "49":
        #     record = record._replace(pollingstationpostcode="DN41 8AX")

        # # T.A. CENTRE, WESTWARD HO, GRIMSBY, DN34 5AE (id: 57)
        # if record.pollingvenueid == "57":
        #     record = record._replace(pollingstationpostcode="DN34 5AT")

        # # PORTACABIN, SCARTHO HALL, MATTHEW TELFORD PARK, GRIMSBY, DN33 2DU (id: 131)
        # if record.pollingvenueid == "131":
        #     record = record._replace(pollingstationpostcode="DN33 2DZ")

        # # ST GILES PARISH ROOM, CHURCH LANE, GRIMSBY, DN33 2EY (id: 64)
        # if record.pollingvenueid == "64":
        #     record = record._replace(pollingstationpostcode="DN33 2EU")

        # # ST GILES PARISH ROOM, CHURCH LANE, GRIMSBY, DN33 2EY (id: 64)
        # if record.pollingvenueid == "64":
        #     record = record._replace(pollingstationpostcode="DN33 2EU")

        # # ST MARTIN'S CHURCH, SUTCLIFFE AVENUE, GRIMSBY, DN33 1AE (id: 68)
        # if record.pollingvenueid == "68":
        #     record = record._replace(pollingstationpostcode="DN33 2AD")

        # # ALL SAINTS CHURCH HALL, HIGH STREET, WALTHAM, DN37 0PN (id: 80)
        # if record.pollingvenueid == "80":
        #     record = record._replace(pollingstationpostcode="DN37 0PL")

        # # WEST MARSH FAMILY HUB, MACAULAY STREET, GRIMSBY, DN31 2ES (id: 85)
        # if record.pollingvenueid == "85":
        #     record = record._replace(pollingstationpostcode="DN31 2EP")

        # # STANFORD CENTRE, (LACEBY LIBRARY), COOPER LANE, LACEBY, DN37 7AX (id: 94)
        # if record.pollingvenueid == "94":
        #     record = record._replace(pollingstationpostcode="DN37 7AY")

        # # ST HELEN'S CHURCH, CHURCH LANE, BARNOLDBY LE BECK, DN37 0AZ (id: 87)
        # if record.pollingvenueid == "87":
        #     record = record._replace(pollingstationpostcode="DN37 0BA")

        # # FARM OFFICE (FENWICK BROS), BEELSBY HOUSE FARM, BEELSBY, DN37 0TL (id: 88)
        # if record.pollingvenueid == "88":
        #     record = record._replace(pollingstationpostcode="DN37 0TN")

        # # STANFORD CENTRE, (LACEBY LIBRARY), COOPER LANE, LACEBY, DN37 7AX (id: 94)
        # if record.pollingvenueid == "94":
        #     record = record._replace(pollingstationpostcode="DN37 7AY")
        return super().station_record_to_dict(record)
