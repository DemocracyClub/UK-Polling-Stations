from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "RUN"
    addresses_name = (
        "2021-03-03T10:09:37.682656/Runnymede Democracy_Club__06May2021 (1).tsv"
    )
    stations_name = (
        "2021-03-03T10:09:37.682656/Runnymede Democracy_Club__06May2021 (1).tsv"
    )
    elections = ["2021-05-06"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10002019662",  # MOBILE HOME GREENACRES BITTAMS LANE, CHERTSEY
            "10092959794",  # ACCOMMODATION AT THE BLACK PRINCE WOODHAM LANE, ADDLESTONE
        ]:
            return None

        if record.addressline6 in ["KT16 8QD", "KT16 8AG"]:
            return None

        return super().address_record_to_dict(record)
