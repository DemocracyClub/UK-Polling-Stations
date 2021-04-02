from data_importers.ems_importers import BaseHalaroseCsvImporter

STG_ADMINAREAS = (
    "Stirling",
    "Stirling Ward 1",
    "Stirling Ward 2",
    "Stirling Ward 3",
    "Stirling Ward 4",
    "Stirling Ward 5",
    "Stirling Ward 6",
    "Stirling Ward 7",
    "Callander",
    "Crianlarich",
    "Killin",
    "Lochearnhead",
    "Dunblane",
    "Doune",
)

STG_EXCLUDE_STATIONS = ()

STG_INCLUDE_STATIONS = (
    "Cowie Community Centre",
    "Balfour Centre",
    "Bannockburn Community Centre",
)


class Command(BaseHalaroseCsvImporter):
    council_id = "STG"
    addresses_name = "2021-04-01T20:40:33.112986/Central Scotland polling_station_export-2021-03-31.csv"
    stations_name = "2021-04-01T20:40:33.112986/Central Scotland polling_station_export-2021-03-31.csv"
    elections = ["2021-05-06"]

    def station_record_to_dict(self, record):
        if (
            (record.adminarea not in STG_ADMINAREAS)
            and (record.pollingstationname not in STG_INCLUDE_STATIONS)
            or (record.pollingstationname in STG_EXCLUDE_STATIONS)
        ):
            return None
        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        if (
            (record.adminarea not in STG_ADMINAREAS)
            and (record.pollingstationname not in STG_INCLUDE_STATIONS)
            or (record.pollingstationname in STG_EXCLUDE_STATIONS)
        ):
            return None

        if record.housepostcode in ["FK9 4JL", "FK8 1TX", "FK7 0LS", "FK17 8HR"]:
            return None
        return super().address_record_to_dict(record)
