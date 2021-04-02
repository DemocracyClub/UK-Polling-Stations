from data_importers.ems_importers import BaseHalaroseCsvImporter

FAL_ADMINAREAS = (
    "Bo'ness",
    "Bonnybridge",
    "Denny",
    "Falkirk Ward 1",
    "Falkirk Ward 2",
    "Falkirk Ward 3",
    "Falkirk Ward 4",
    "Falkirk Ward 5",
    "Falkirk Ward 6",
    "Falkirk Ward 7",
    "Falkirk Ward 8",
    "Falkirk Ward 9",
    "Falkirk",
    "Grangemouth",
    "Larbert",
)
FAL_INCLUDE_STATIONS = [
    "Maddiston Old Folks Hall",
    "Deanburn Primary School",
    "Blackness Community Hall",
]
FAL_EXCLUDE_STATIONS = [
    "Cowie Community Centre",
    "Balfour Centre",
    "Bannockburn Community Centre",
]


class Command(BaseHalaroseCsvImporter):
    council_id = "FAL"
    addresses_name = "2021-04-01T20:39:48.865108/Central Scotland polling_station_export-2021-03-31.csv"
    stations_name = "2021-04-01T20:39:48.865108/Central Scotland polling_station_export-2021-03-31.csv"
    elections = ["2021-05-06"]

    def station_record_to_dict(self, record):
        if (
            (record.adminarea not in FAL_ADMINAREAS)
            and (record.pollingstationname not in FAL_INCLUDE_STATIONS)
            or (record.pollingstationname in FAL_EXCLUDE_STATIONS)
        ):
            return None
        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        if (
            (record.adminarea not in FAL_ADMINAREAS)
            and (record.pollingstationname not in FAL_INCLUDE_STATIONS)
            or (record.pollingstationname in FAL_EXCLUDE_STATIONS)
        ):
            return None

        if record.housepostcode in [
            "FK2 7FG",
            "FK6 5EP",
            "FK2 7YN",
        ]:
            return None

        return super().address_record_to_dict(record)
