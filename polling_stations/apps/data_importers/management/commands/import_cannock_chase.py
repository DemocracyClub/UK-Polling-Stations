from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "CAN"
    addresses_name = (
        "2026-05-07/2026-03-23T10:54:14.941988/Democracy_Club__07May2026.tsv"
    )
    stations_name = (
        "2026-05-07/2026-03-23T10:54:14.941988/Democracy_Club__07May2026.tsv"
    )
    elections = ["2026-05-07"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "100032224228",  # 179 HEDNESFORD ROAD, HEATH HAYES, CANNOCK
            "100031617493",  # 22 BROWNHILLS ROAD, NORTON CANES, CANNOCK
            "10091050996",  # MOBILE HOME AT PLOT 6 LEACROFT END LICHFIELD ROAD, CANNOCK
        ]:
            return None

        if record.addressline6 in [
            # splits
            "WS12 3YG",
            "WS11 9NW",
            # look wrong
            "WS11 9AD",
            "WS11 9SD",
        ]:
            return None

        return super().address_record_to_dict(record)
