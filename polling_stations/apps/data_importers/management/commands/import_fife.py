from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "FIF"
    addresses_name = "2024-07-04/2024-06-20T14:09:30.467880/Polling Districts UTF-8.csv"
    stations_name = "2024-07-04/2024-06-20T14:09:30.467880/Polling Stations.csv"
    elections = ["2024-07-04"]

    def station_record_to_dict(self, record):
        # The following coordinte changes are from the council:

        # ST ANDREWS-ERSKINE PARISH CHURCH HALL, ROBERTSON ROAD, DUNFERMLINE
        if record.stationcode == "26":
            record = record._replace(xordinate="310949.65", yordinate="688612.91")

        # OAKLEY CENTRE, STATION ROAD, OAKLEY (two polling stations)
        if record.stationcode in [
            "12",
            "11",
        ]:
            record = record._replace(xordinate="302501.68", yordinate="689325.09")

        # BRITISH LEGION, THE CROSS, KENNOWAY
        if record.stationcode == "302":
            record = record._replace(xordinate="335047.31", yordinate="702501.42")

        # removes map for the following station pending council response:
        # TORBAIN PARISH CHURCH HALL, CARRON PLACE, KIRKCALDY, FIFE KY2 6PS
        if record.stationcode in [
            "117",
            "118",
            "119",
        ]:
            record = record._replace(xordinate="", yordinate="")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "320329489",  # 34 RITCHIE AVENUE, DUNFERMLINE
            "320329487",  # 32 RITCHIE AVENUE, DUNFERMLINE
        ]:
            return None

        if record.postcode in [
            "KY12 8DT",  # split
        ]:
            return None

        return super().address_record_to_dict(record)
