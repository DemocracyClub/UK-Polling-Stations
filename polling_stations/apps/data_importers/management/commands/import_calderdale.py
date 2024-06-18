from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "CLD"
    addresses_name = "2024-07-04/2024-06-06T14:49:45.071526/CMBC_Democracy_Club_PS_Extract_PollingDistricts_UKPGE.csv"
    stations_name = "2024-07-04/2024-06-06T14:49:45.071526/CMBC_Democracy_Club_PS_Extract_PollingStations_UKPGE.csv"
    elections = ["2024-07-04"]

    def station_record_to_dict(self, record):
        # LEE MOUNT BAPTIST CHURCH, MELBOURNE STREET, LEE MOUNT, HALIFAX, WEST YORKSHIRE HX3 5BQ
        if record.stationcode == "60JB":
            record = record._replace(xordinate="408412")
            record = record._replace(yordinate="426427")

        # The following are coord amendments from the council:

        # ST AUGUSTINE'S CENTRE, HANSON LANE, HALIFAX, HX1 5PG
        if record.stationcode == "68KE":
            record = record._replace(xordinate="408189")
            record = record._replace(yordinate="425465")
        # PELLON BAPTIST SUNDAY SCHOOL, SPRING HALL LANE, HALIFAX, HX1 4UA
        if record.stationcode in [
            "110SA",
            "114SE",
        ]:
            record = record._replace(xordinate="407498")
            record = record._replace(yordinate="425770")
        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        if record.uprn in [
            "10093206213",  # 1 PARKIN LANE, TODMORDEN
            "10093208972",  # GREAT LEAR INGS BARN, HEPTONSTALL, HEBDEN BRIDGE
        ]:
            return None

        if record.postcode in [
            "HX2 0UW",  # suspect
        ]:
            return None

        return super().address_record_to_dict(record)
