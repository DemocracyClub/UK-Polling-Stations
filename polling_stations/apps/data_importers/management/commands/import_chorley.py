from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "CHO"
    addresses_name = "2024-07-04/2024-06-04T09:29:17.473081/CHO_combined.csv"
    stations_name = "2024-07-04/2024-06-04T09:29:17.473081/CHO_combined.csv"
    elections = ["2024-07-04"]

    def station_record_to_dict(self, record):
        # TEMPORARY MOBILE STATION, WHITE HORSE CAR PARK, RAWLINSON LANE, HEATH CHARNOCK, CHORLEY, LANCS PR6 9LJ
        if record.pollingstationnumber == "35":
            record = record._replace(pollingstationpostcode="PR6 9JS")

        # LANCASTER WAY COMMUNITY CENTRE, LANCASTER WAY (OFF ORDINANCE ROAD), BUCKSHAW VILLAGE, CHORLEY, PR7 7GA (id: 95)
        if record.pollingvenueid == "95":
            record = record._replace(pollingstationpostcode="PR7 7LJ")

        # The following station's postcode has been confirmed by the council:
        # BUCKSHAW ROF SCOUT GROUP, MILE STONE MEADOW, EUXTON, CHORLEY, PR7 6FX (id: 97)

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "100010387618",  # MILLSTONE HOUSE, THE GREEN, ECCLESTON, CHORLEY
            "10094693572",  # 64B MARKET STREET, CHORLEY
        ]:
            return None

        if record.housepostcode in [
            # split
            "PR7 2QL",
            "PR6 0HT",
            # suspect
            "PR26 9HE",
        ]:
            return None

        return super().address_record_to_dict(record)
