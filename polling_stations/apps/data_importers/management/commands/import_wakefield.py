from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "WKF"
    addresses_name = "2023-05-04/2023-04-04T11:04:06.375522/20230320_DemocracyClubPollingDistricts_DistrictElections4May2023.csv"
    stations_name = "2023-05-04/2023-04-04T11:04:06.375522/20230320_DemocracyClubPollingStations_DistrictElections4May2023.csv"
    elections = ["2023-05-04"]

    def address_record_to_dict(self, record):
        uprn = record.uprn.lstrip("0").strip()

        if uprn in [
            "63205108",  # THE COTTAGE, WENTBRIDGE, PONTEFRACT
            "63111468",  # 14 THE GREEN, SOUTH KIRKBY, PONTEFRACT
            "63200615",  # FLAT 1 PLUMPTON STREET, WAKEFIELD
            "63194364",  # 2 STARLING WAY, CASTLEFORD
        ]:
            return None

        if record.postcode.strip() in [
            # split
            "WF2 6JA",
            "WF5 0RT",
            # wrong
            "WF9 2FB",
            "WF9 2FA",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        if record.stationcode in [
            "152-20WF",  # WESTGATE COMMON W.M.C.
            "23-03NG",  # THREE LANE ENDS ACADEMY
        ]:
            record = record._replace(xordinate="", yordinate="")

        return super().station_record_to_dict(record)
