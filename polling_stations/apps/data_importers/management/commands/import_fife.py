from data_importers.ems_importers import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "FIF"
    addresses_name = "2021-04-12T09:21:22.730934/Fife E8 DC Polling Districts.csv"
    stations_name = "2021-04-12T09:21:22.730934/Fife E8 DC Polling Stations.csv"
    elections = ["2021-05-06"]

    def station_record_to_dict(self, record):

        # LOCHGELLY TOWN HALL BANK STREET LOCHGELLY KY5 9QQ
        if record.stationcode in [
            "130",
            "131",
            "132",
        ]:
            record = record._replace(
                placename="LOCHGELLY CENTRE", add1="BANK STREET", postcode=" KY5 9RD"
            )

        return super().station_record_to_dict(record)
