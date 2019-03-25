from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000179"
    addresses_name = (
        "local.2019-05-02/Version 1/Democracy Club Data South Oxfordshire.tsv"
    )
    stations_name = (
        "local.2019-05-02/Version 1/Democracy Club Data South Oxfordshire.tsv"
    )
    elections = ["local.2019-05-02"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)

        # 10090812631 assigned to polling station 6782. Rest of postcode assigned to 6607.
        # 10033011944 assigned to polling station 6765. Rest of postcode assigned to 6739.
        if rec:
            if rec["postcode"] in ["RG8 9EY", "OX49 5BZ"]:
                return None

        return rec
