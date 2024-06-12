from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "NED"
    addresses_name = (
        "2024-07-04/2024-06-12T11:55:09.054594/Democracy_Club__04July2024.tsv"
    )
    stations_name = (
        "2024-07-04/2024-06-12T11:55:09.054594/Democracy_Club__04July2024.tsv"
    )
    elections = ["2024-07-04"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10034037761",  # GLENDALE HOUSE, STONEDGE, ASHOVER, CHESTERFIELD
        ]:
            return None

        if record.addressline6 in [
            # suspect
            "S45 0LN",
        ]:
            return None

        return super().address_record_to_dict(record)
