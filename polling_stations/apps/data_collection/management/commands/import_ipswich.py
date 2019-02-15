from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000202"
    addresses_name = "local.2019-05-02/Version 1/Democracy_Club__02May2019 Ipswich.CSV"
    stations_name = "local.2019-05-02/Version 1/Democracy_Club__02May2019 Ipswich.CSV"
    elections = ["local.2019-05-02"]
