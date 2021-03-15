from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "WDE"
    addresses_name = (
        "2021-03-12T10:39:08.998016/West Devon Democracy_Club__06May2021.tsv"
    )
    stations_name = (
        "2021-03-12T10:39:08.998016/West Devon Democracy_Club__06May2021.tsv"
    )
    elections = ["2021-05-06"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10013758398",  # MOWHAY BARN, HIGHER CARLEY BARNS, LIFTON
            "10001332226",  # BERRYDOWN STABLES, EXBOURNE, OKEHAMPTON
            "10013751665",  # HOMEFIELD, DREWSTEIGNTON, EXETER
            "10001330732",  # ROWDEN, BRIDESTOWE, OKEHAMPTON
        ]:
            return None

        if record.addressline6 in [
            "EX20 3NX",
            "EX20 3NW",
            "EX20 1QB",
            "EX20 2TP",
            "EX20 2SD",
            "EX20 1SY",
            "EX20 2NF",
            "PL19 9HA",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # Lifton Community Centre Park Wood Rise Lifton PL16 0AL
        if record.polling_place_id == "8001":
            record = record._replace(polling_place_postcode="PL16 0LA")

        return super().station_record_to_dict(record)
