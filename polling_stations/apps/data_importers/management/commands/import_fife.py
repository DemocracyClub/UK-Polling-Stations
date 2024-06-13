from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "FIF"
    addresses_name = "2024-07-04/2024-06-20T14:09:30.467880/Polling Districts UTF-8.csv"
    stations_name = "2024-07-04/2024-06-20T14:09:30.467880/Polling Stations.csv"
    elections = ["2024-07-04"]

    def station_record_to_dict(self, record):
        # ST ANDREWS-ERSKINE PARISH CHURCH HALL, ROBERTSON ROAD, DUNFERMLINE
        if record.stationcode == "26":
            record = record._replace(xordinate="", yordinate="")

        # OAKLEY CENTRE, STATION ROAD, OAKLEY (two polling stations)
        if record.stationcode in [
            "12",
            "11",
        ]:
            record = record._replace(xordinate="", yordinate="")

        # BRITISH LEGION, THE CROSS, KENNOWAY
        if record.stationcode == "302":
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
