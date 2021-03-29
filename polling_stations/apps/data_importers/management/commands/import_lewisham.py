from django.contrib.gis.geos import Point
from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "LEW"
    addresses_name = "2021-03-25T11:53:33.439549/Democracy_Club__06May2021.tsv"
    stations_name = "2021-03-25T11:53:33.439549/Democracy_Club__06May2021.tsv"
    elections = ["2021-05-06"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):

        # Sir Francis Drake Primary School
        if record.polling_place_id == "16834":
            rec = super().station_record_to_dict(record)
            rec["location"] = Point(-0.041453, 51.485092, srid=4326)
            return rec

        # All Saints Community Centre
        if record.polling_place_id == "16883":
            rec = super().station_record_to_dict(record)
            rec["location"] = Point(-0.048807, 51.476468, srid=4326)
            return rec

        # Catford Wanderers Sports Club Beckenham Hill Road (Homebase entrance) London SE6 2NU
        if record.polling_place_id == "17989":
            record = record._replace(polling_place_postcode="SE6 3NU")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "100021990765",  # 173D NEW CROSS ROAD, LONDON
            "100021990762",  # 173A NEW CROSS ROAD, LONDON
            "100021990764",  # 173C NEW CROSS ROAD, LONDON
            "10023226417",  # FLAT 31B, FAIRLAWN MANSIONS, NEW CROSS ROAD, LONDON
            "10023226416",  # FLAT 31A, FAIRLAWN MANSIONS, NEW CROSS ROAD, LONDON
            "100022832913",  # 5 COACH HOUSE MEWS, LONDON
            "100022017435",  # 1 WALLER ROAD, LONDON
            "100022017436",  # 3 WALLER ROAD, LONDON
            "100021951182",  # FLAT B, 71 DENNETT'S ROAD, LONDON
            "100021957218",  # 79 ERLANGER ROAD, LONDON
            "100021990842",  # 237B NEW CROSS ROAD, LONDON
            "100021990833",  # 233A NEW CROSS ROAD, LONDON
            "100021990809",  # UPPER FLOOR FLAT, 217 NEW CROSS ROAD, LONDON
            "100021990838",  # 235B NEW CROSS ROAD, LONDON
            "100021990839",  # 235C NEW CROSS ROAD, LONDON
            "100021990834",  # 233B NEW CROSS ROAD, LONDON
            "100021990837",  # 235A NEW CROSS ROAD, LONDON
            "100021990841",  # BASEMENT FLAT, 237 NEW CROSS ROAD, LONDON
            "100021990808",  # 217A NEW CROSS ROAD, LONDON
            "100021990842",  # 237B NEW CROSS ROAD, LONDON
            "10023225635",  # 22 ASHBY ROAD, LONDON
            "10093392954",  # 18 ASHBY ROAD, LONDON
            "100021935766",  # 128A BREAKSPEARS ROAD, LONDON
            "100021935767",  # 128B BREAKSPEARS ROAD, LONDON
            "100023271682",  # 353 BROCKLEY ROAD, LONDON
            "10093390741",  # FIRST FLOOR FLAT 2 353 BROCKLEY ROAD, CROFTON PARK, LONDON
            "100021937686",  # FLAT 1 353 BROCKLEY ROAD, CROFTON PARK, LONDON
            "200000559234",  # FLAT 5 353 BROCKLEY ROAD, CROFTON PARK, LONDON
            "100021937688",  # 355A BROCKLEY ROAD, LONDON
            "100023234043",  # ST. MARGARETS VISITOR CENTRE, BRANDRAM ROAD, LONDON
            "100021935200",  # 2 BRANDRAM ROAD, LONDON
            "100021935291",  # 2 BRANDRAM MEWS, BRANDRAM ROAD, LONDON
            "100021935198",  # 2A BRANDRAM ROAD, LONDON
            "100023234264",  # 2B BRANDRAM ROAD, LONDON
            "100021931415",  # FLAT D, 33 BELMONT PARK, LONDON
            "100021931413",  # FLAT B, 33 BELMONT PARK, LONDON
            "100021931412",  # FLAT A, 33 BELMONT PARK, LONDON
            "100021931414",  # FLAT C, 33 BELMONT PARK, LONDON
            "100021931416",  # FLAT E, 33 BELMONT PARK, LONDON
            "100021931417",  # FLAT F, 33 BELMONT PARK, LONDON
            "100021978708",  # 299 LEWISHAM HIGH STREET, HITHER GREEN, LONDON
            "100021977294",  # 158 LEE HIGH ROAD, LONDON
            "200000558488",  # FLAT ABOVE 156 LEE HIGH ROAD, LONDON
            "100021954384",  # FLAT 19 EASTDOWN COURT 1-11 EASTDOWN PARK, HITHER GREEN, LONDON
            "100021954385",  # FLAT 20 EASTDOWN COURT 1-11 EASTDOWN PARK, HITHER GREEN, LONDON
            "100021954375",  # FLAT 10 EASTDOWN COURT 1-11 EASTDOWN PARK, HITHER GREEN, LONDON
            "100021954377",  # FLAT 12 EASTDOWN COURT 1-11 EASTDOWN PARK, HITHER GREEN, LONDON
            "100021954376",  # FLAT 11-15, EASTDOWN COURT 1-11, EASTDOWN PARK, LONDON
            "100021981698",  # 58 LONGHURST ROAD, LONDON
            "200002157666",  # 50B LADYWELL ROAD, LADYWELL, LONDON
            "200002157665",  # 50A LADYWELL ROAD, LADYWELL, LONDON
            "10023229356",  # GROUND FLOOR AND FIRST FLOOR FLAT 20 DARTMOUTH ROAD, LONDON
            "100021950380",  # FLAT ABOVE 182 DARTMOUTH ROAD, LONDON
            "100021950385",  # 190 DARTMOUTH ROAD, LONDON
            "100021950383",  # 188A DARTMOUTH ROAD, LONDON
            "10070493932",  # 186B DARTMOUTH ROAD, LONDON
            "10023225802",  # 186A DARTMOUTH ROAD, LONDON
            "100021950381",  # 184 DARTMOUTH ROAD, LONDON
            "200000561719",  # 1 SYDENHAM PARK MANSIONS HOSTEL SYDENHAM PARK, LONDON
            "200000561743",  # 32 SYDENHAM PARK MANSIONS HOSTEL SYDENHAM PARK, LONDON
            "200002483518",  # 14 SYDENHAM PARK MANSIONS HOSTEL SYDENHAM PARK, LONDON
            "100023278866",  # 3 BROOKDALE ROAD, LONDON
            "100021989292",  # 15 MOUNT PLEASANT ROAD, LONDON
            "100021932193",  # 13A BIRKHALL ROAD, LONDON
            "100023277411",  # LOWER FLAT, 12 BELLINGHAM ROAD, LONDON
            "100023277595",  # UPPER FLAT, 12 BELLINGHAM ROAD, LONDON
            "100023253733",  # FLAT 2, EMBASSY COURT, 34 ST. GERMAN'S ROAD, LONDON
            "10023229662",  # 46 ARBUTHNOT ROAD, LONDON
            "100022010695",  # 11A SYDENHAM ROAD, LONDON
            "100022009747",  # 14 SYDENHAM HILL, LONDON
            "100022011071",  # 4D TALBOT PLACE, BLACKHEATH, LONDON
            "100021990763",  # 173B NEW CROSS ROAD, LONDON
            "100021975224",  # 73A LADYWELL ROAD, LONDON
        ]:
            return None

        if record.addressline6 in [
            "SE4 2EW",
            "SE26 6AA",
            "SE13 6ET",
            "BR1 4PB",
            "SE6 3PL",
        ]:
            return None

        return super().address_record_to_dict(record)
