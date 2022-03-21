from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "GRE"
    addresses_name = (
        "2022-05-05/2022-03-21T14:44:29.868800/Democracy_Club__05May2022.tsv"
    )
    stations_name = (
        "2022-05-05/2022-03-21T14:44:29.868800/Democracy_Club__05May2022.tsv"
    )
    elections = ["2022-05-05"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")
        if uprn in [
            "10010227617",  # 292B PLUMSTEAD COMMON ROAD, PLUMSTEAD
        ]:
            return None

        if record.addressline6 in [
            "SE9 2BU",
        ]:
            return None

        return super().address_record_to_dict(record)
