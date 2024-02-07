from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "NWA"
    addresses_name = (
        "2024-05-02/2024-02-07T08:53:01.197969/Democracy_Club__02May2024.tsv"
    )
    stations_name = (
        "2024-05-02/2024-02-07T08:53:01.197969/Democracy_Club__02May2024.tsv"
    )
    elections = ["2024-05-02"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "100071230930",  # I.S.I LTD, LEA COTTAGE NUNEATON ROAD, ANSLEY
            "200001812992",  # LEA LODGE, ANSLEY, NUNEATON
        ]:
            return None

        if record.addressline6 in [
            # split in council data
            "B46 1BB",
            # suspect
            "CV10 9SW",
            "CV9 3DW",
            "CV9 2PB",
            "CV10 0TB",
            "B76 0DT",
        ]:
            return None

        return super().address_record_to_dict(record)
