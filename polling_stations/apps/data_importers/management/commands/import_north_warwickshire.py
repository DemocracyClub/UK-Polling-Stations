from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "NWA"
    addresses_name = (
        "2025-05-01/2025-02-25T15:07:20.110575/Democracy_Club__01May2025.tsv"
    )
    stations_name = (
        "2025-05-01/2025-02-25T15:07:20.110575/Democracy_Club__01May2025.tsv"
    )
    elections = ["2025-05-01"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "100071230930",  # I.S.I LTD, LEA COTTAGE NUNEATON ROAD, ANSLEY
            "200001812992",  # LEA LODGE, ANSLEY, NUNEATON
            "100071519252",  # SLOWLEY HALL, TAMWORTH ROAD, FILLONGLEY, COVENTRY
            "100071232116",  # OAKLEAVES, BIRCHLEY HEATH ROAD, BIRCHLEY HEATH, NUNEATON
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
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # The following Warning was investigated and ignored:
        # WARNING: Polling station Dosthill Boys Club (4864) is in Tamworth Borough Council (TAW)
        # but target council is North Warwickshire Borough Council (NWA) - manual check recommended

        return super().station_record_to_dict(record)
