from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "NWA"
    addresses_name = (
        "2023-05-04/2023-01-18T11:33:19.887373/Democracy_Club__04May2023.tsv"
    )
    stations_name = (
        "2023-05-04/2023-01-18T11:33:19.887373/Democracy_Club__04May2023.tsv"
    )
    elections = ["2023-05-04"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10001177416",  # WARREN FARM HOUSE, KINWALSEY LANE, MERIDEN, COVENTRY
            "100071230930",  # I.S.I LTD, LEA COTTAGE NUNEATON ROAD, ANSLEY
            "200001812992",  # LEA LODGE, ANSLEY, NUNEATON
            "10001177408",  # CHURCH TREE BARN, KINWALSEY LANE, MERIDEN, COVENTRY
        ]:
            return None

        if record.addressline6 in [
            "B46 1BB",  # split in council data
            "ST4 7LG",
            "CV10 9SW",
        ]:
            return None

        return super().address_record_to_dict(record)
