from data_collection.management.commands import (
    BaseXpressDCCsvInconsistentPostcodesImporter,
)


class Command(BaseXpressDCCsvInconsistentPostcodesImporter):
    council_id = "E07000052"
    addresses_name = "parl.2017-06-08/Version 1/Democracy_Club__08June2017WDDC.TSV"
    stations_name = "parl.2017-06-08/Version 1/Democracy_Club__08June2017WDDC.TSV"
    elections = ["parl.2017-06-08"]
    csv_delimiter = "\t"

    station_postcode_search_fields = [
        "polling_place_postcode",
        "polling_place_address_4",
        "polling_place_address_3",
        "polling_place_address_2",
        "polling_place_address_1",
    ]
