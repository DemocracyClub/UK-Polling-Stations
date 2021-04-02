from data_importers.ems_importers import BaseDemocracyCountsCsvImporter

IVC_STATIONCODES = (
    "IG36_1",
    "IG17_3",
    "IG05_1",
    "IG26_2",
    "IG21_1",
    "IG19_3",
    "BETHESDA_1",
    "STCOLUMBAS_4",
    "IG23_1",
    "IG23_2",
    "IG27_3",
    "IG32_1",
    "IG30_2",
    "IG01_1",
    "IG09_1",
    "IG30_1",
    "IG10_2",
    "IG13_1",
    "IG12_2",
    "IG36_2",
    "IG06_1",
    "IG29_1",
    "IG17_2",
    "IG13_2",
    "IG03_1",
    "IG08_2",
    "IG31_2",
    "IG02_1",
    "IG02_2",
    "IG26_1",
    "IG11_1",
    "IG21_2",
    "IG35_1",
    "IG33_1",
    "IG07_1",
    "IG06_3",
    "IG27_2",
    "IG15_1",
    "IG23_3",
    "IG33_2",
    "IG14_2",
    "IG08_1",
    "IG19_1",
    "IG17_1",
    "IG34_1",
    "IG24_1",
    "IG22_1",
    "IG09_2",
    "IG28_1",
    "IG20_2",
    "IG11_2",
    "IG16_2",
    "IG04_1",
    "STCOLUMBAS_3",
    "IG03_2",
    "IG25_1",
    "IG28_2",
    "IG12_1",
    "IG04_2",
    "IG06_2",
    "IG30_3",
    "IG19_2",
    "IG35_2",
    "IG20_1",
    "IG31_1",
    "IG27_1",
    "IG14_1",
    "IG18_2",
    "IG07_2",
    "IG10_1",
    "IG16_1",
    "IG01_2",
    "STCOLUMBAS_2",
    "STCOLUMBAS_1",
    "IG10_3",
    "IG22_2",
    "IG33_3",
    "IG18_1",
)


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "IVC"
    addresses_name = (
        "2021-03-25T10:48:11.214321/Refrew DemocracyClub_PollingDistricts.csv"
    )
    stations_name = (
        "2021-03-25T10:48:11.214321/Refrew DEmocracyClub_PollingStations.csv"
    )
    elections = ["2021-05-06"]

    def address_record_to_dict(self, record):
        if record.stationcode not in IVC_STATIONCODES:
            return None
        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        if record.stationcode not in IVC_STATIONCODES:
            return None
        if record.stationcode in [
            "IG07_1",  # ST JOHN'S CHURCH HALL ST JOHN'S CHURCH HALL
            "IG07_2",  # ST JOHN'S CHURCH HALL ST JOHN'S CHURCH HALL
        ]:
            record = record._replace(xordinate="")
            record = record._replace(yordinate="")
        return super().station_record_to_dict(record)
