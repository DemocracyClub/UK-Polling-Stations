from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000210"
    addresses_name = (
        "local.2018-05-03/Version 1/Democracy_Club__03May2018 Mole Valley (1).csv"
    )
    stations_name = (
        "local.2018-05-03/Version 1/Democracy_Club__03May2018 Mole Valley (1).csv"
    )
    elections = ["local.2018-05-03"]

    def address_record_to_dict(self, record):

        # All of the UPRN data from Mole Valley is a bit dubious.
        # For safety I'm just going to ignore them all
        record = record._replace(property_urn="")

        return super().address_record_to_dict(record)
