from data_importers.management.commands import BaseXpressWebLookupCsvImporter
from django.contrib.gis.geos import Point


class Command(BaseXpressWebLookupCsvImporter):
    council_id = "UTT"
    addresses_name = "2023-05-04/2023-02-24T14:41:13.026306/PropertyPostCodePollingStationWebLookup-2023-02-24.TSV"
    stations_name = "2023-05-04/2023-02-24T14:41:13.026306/PropertyPostCodePollingStationWebLookup-2023-02-24.TSV"
    elections = ["2023-05-04"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "200004270735",  # B LODGE, EASTON LODGE, LITTLE EASTON, DUNMOW
            "10002182834",  # ANNEXE AT PLEDGDON LODGE BRICK END ROAD, HENHAM
            "100091279626",  # WAPLES MILL, ONGAR ROAD, MARGARET RODING, DUNMOW
            "200004273362",  # WOODLANDS, TAKELEY, BISHOP'S STORTFORD
        ]:
            return None

        if record.postcode in [
            "CM7 4PT",  # split
            "CM22 6FG",
            "CM22 6TW",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        if record.pollingplaceid in [
            "1127",  # Langley Community Centre, Langley Upper Green, Saffron Walden, CB11 4RU
            "1292",  # The Community Hall at Carver Barracks, Off Elder Street, Wimbish, Saffron Walden, CB10 2YB
            "1275",  # Leaden Roding Village Hall,  Stortford Road,  Leaden Roding,  Dunmow
            "1210",  # Council Offices,  London Road,  London Road, Saffron Walden, Essex
        ]:
            record = record._replace(pollingplaceaddress7="")

        rec = super().station_record_to_dict(record)

        # St. Mary`s CoE Foundation Primary School, Stansted School Hall Hampton Road Stansted CM24 8FE
        if rec["internal_council_id"] == "1301":
            rec["uprn"] = "10090833547"
            rec["location"] = Point(0.19813481644966854, 51.895925525754386, srid=4326)

        # Sewards End Village Hall,	Radwinter Road,	Sewards End	Saffron Walden
        if rec["internal_council_id"] == "1119":
            rec["location"] = Point(0.288313, 52.021565, srid=4326)

        # Hatfield Heath Village Hall, The Heath, Hatfield Heath, Bishop`s Stortford
        if rec["internal_council_id"] == "1174":
            rec["location"] = Point(0.20601490457884916, 51.813635643771676, srid=4326)

        # Hatfield Broad Oak Village Hall,  Cage End, Hatfield Broad Oak, Bishop`s Stortford
        if rec["internal_council_id"] == "1166":
            rec["location"] = Point(0.2420393664199665, 51.82366629430033, srid=4326)

        # St. Mary`s Church Hall,  Birchanger Lane, Birchanger, Bishops Stortford
        if rec["internal_council_id"] == "1299":
            rec["location"] = Point(0.1901025089340043, 51.884113757259236, srid=4326)

        # Farnham Village Hall,  Rectory Lane, Farnham, Bishop`s Stortford
        if rec["internal_council_id"] == "1233":
            rec["location"] = Point(0.14184549037960656, 51.902562759160546, srid=4326)

        # Broxted Village Hall,  Browns End Road, Broxted, Dunmow
        if rec["internal_council_id"] == "1242":
            rec["location"] = Point(0.28619090086472165, 51.90857290858807, srid=4326)

        # Little Canfield Village Hall,  Stortford Road, Little Canfield, Dunmow
        if rec["internal_council_id"] == "1244":
            rec["location"] = Point(0.3075562039168354, 51.868068473426916, srid=4326)

        # Marquee at The Three Horseshoes, Mole Hill Green, Takeley
        if rec["internal_council_id"] == "1327":
            rec["location"] = Point(0.2705578586009892, 51.89910159079529, srid=4326)

        # Great Easton Village Hall,  Rebecca Meade, Great Easton, Dunmow
        if rec["internal_council_id"] == "1258":
            rec["location"] = Point(0.33530918605452925, 51.90531563768987, srid=4326)

        # Hadstock Village Hall, Church Lane, Hadstock, CB21 4PH
        if rec["internal_council_id"] == "1114":
            rec["location"] = Point(0.27383219315604296, 52.07891625101157, srid=4326)

        return rec
