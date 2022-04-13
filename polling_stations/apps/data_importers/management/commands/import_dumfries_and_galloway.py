from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "DGY"
    addresses_name = (
        "2022-05-05/2022-04-13T11:33:08.115803/April 22 Polling Districts.csv"
    )
    stations_name = (
        "2022-05-05/2022-04-13T11:33:08.115803/April 2022 Polling Stations.csv"
    )
    elections = ["2022-05-05"]

    def station_record_to_dict(self, record):
        # MIDDLEBIE COMMUNITY CENTRE, MIDDLEBIE, LOCKERBIE
        if record.stationcode == "AEE8":
            record = record._replace(xordinate="")
            record = record._replace(yordinate="")

        # THORNHILL COMMUNITY CENTRE, EAST BACK STREET, THORNHILL
        if record.stationcode == "MUN11":
            record = record._replace(xordinate="")
            record = record._replace(yordinate="")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        if record.postcode in ["DG8 0BZ"]:
            return None

        return super().address_record_to_dict(record)
