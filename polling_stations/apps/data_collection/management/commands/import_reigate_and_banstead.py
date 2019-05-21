from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000211"
    addresses_name = (
        "europarl.2019-05-23/Version 2/Democracy_Club__23May2019Reigate.tsv"
    )
    stations_name = "europarl.2019-05-23/Version 2/Democracy_Club__23May2019Reigate.tsv"
    elections = ["europarl.2019-05-23"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "68178079",
            "68178081",
            "68178085",
            "68178086",
            "68178087",
            "68178088",
        ]:
            return None

        return rec
