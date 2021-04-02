from data_importers.ems_importers import BaseDemocracyCountsCsvImporter

ERW_STATIONCODES = (
    "53",
    "58",
    "2",
    "42",
    "48",
    "29",
    "34",
    "44",
    "51",
    "CROSSAPS_1",
    "25",
    "54",
    "35",
    "45",
    "46",
    "10",
    "NEILSTONPS_3",
    "7",
    "38",
    "11",
    "23",
    "5",
    "NEILSTONPS_4",
    "MUREHALL_1",
    "37",
    "13",
    "AUCHENBACK_3",
    "52",
    "3",
    "8",
    "21",
    "AUCHENBACK_2",
    "49",
    "30",
    "4",
    "STANREWCH_3",
    "CROSSAPS_3",
    "CROSSAPS_4",
    "28",
    "61",
    "DALMENYCC_2",
    "9",
    "CROSSAPS_2",
    "STANREWCH_1",
    "41",
    "59",
    "16",
    "CARLIBARPS_1",
    "39",
    "36",
    "DALMENYCC_1",
    "24",
    "1",
    "55",
    "20",
    "47",
    "15",
    "AUCHENBACK_4",
    "50",
    "32",
    "NEILSTONPS_5",
    "CARLIBARPS_3",
    "CARLIBARPS_2",
    "NEILSTONPS_1",
    "31",
    "56",
    "14",
    "AUCHENBACK_1",
    "19",
    "22",
    "60",
    "26",
    "18",
    "NEILSTONPS_2",
    "6",
    "57",
    "STANREWCH_2",
    "27",
    "17",
    "40",
    "12",
    "43",
    "33",
)


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "ERW"
    addresses_name = (
        "2021-03-25T10:46:11.501580/Refrew DemocracyClub_PollingDistricts.csv"
    )
    stations_name = (
        "2021-03-25T10:46:11.501580/Refrew DEmocracyClub_PollingStations.csv"
    )
    elections = ["2021-05-06"]

    def address_record_to_dict(self, record):
        if record.stationcode not in ERW_STATIONCODES:
            return None
        if record.postcode == "G76 8RW":
            return None
        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        if record.stationcode not in ERW_STATIONCODES:
            return None
        return super().station_record_to_dict(record)
