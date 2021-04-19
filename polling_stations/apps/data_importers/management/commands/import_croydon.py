from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "CRY"
    addresses_name = (
        "2021-04-16T11:52:42.569584/Croydon 3Democracy_Club__06May2021.tsv V2.tsv"
    )
    stations_name = (
        "2021-04-16T11:52:42.569584/Croydon 3Democracy_Club__06May2021.tsv V2.tsv"
    )
    elections = ["2021-05-06"]
    csv_delimiter = "\t"
    csv_encoding = "windows-1252"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "200001221192",  # 141 BRIGHTON ROAD, PURLEY
            "10093049201",  # 16A LIMPSFIELD ROAD, SOUTH CROYDON
            "10093049200",  # 16 LIMPSFIELD ROAD, SOUTH CROYDON
            "100020680814",  # FLAT 2 9A LIMPSFIELD ROAD, SOUTH CROYDON
            "100020680813",  # FLAT 1 9A LIMPSFIELD ROAD, SOUTH CROYDON
            "100020680810",  # 3A LIMPSFIELD ROAD, SOUTH CROYDON
            "100020584917",  # WEST LODGE, BISHOPS WALK, CROYDON
            "100020676357",  # 18A CROHAM ROAD, SOUTH CROYDON
            "100022908056",  # 4 HIGH TREES, CROYDON
            "100022908054",  # 2 HIGH TREES, CROYDON
            "100022908055",  # 3 HIGH TREES, CROYDON
            "10093046375",  # 237A SYDENHAM ROAD, CROYDON
            "100020690731",  # 39 BRICKFIELD ROAD, THORNTON HEATH
            "100020572288",  # 71 BRIGHTON ROAD, COULSDON
        ]:
            return None

        if record.addressline6 in [
            "CR7 7JJ",
            "CR0 1ND",
            "CR0 5RN",
            "CR0 2JH",
            "CR2 0JB",
            "CR8 2BA",
            "CR0 0NX",
            "CR0 8RG",
            "SE19 3FB",
        ]:
            return None

        return super().address_record_to_dict(record)
