from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "BRM"
    addresses_name = (
        "2023-05-04/2023-04-05T11:21:23.640951/Bromsgrove Democracy_Club__04May2023.CSV"
    )
    stations_name = (
        "2023-05-04/2023-04-05T11:21:23.640951/Bromsgrove Democracy_Club__04May2023.CSV"
    )
    elections = ["2023-05-04"]

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10090741909",  # THE OLD FORGE, BROMSGROVE ROAD, CLENT, STOURBRIDGE
        ]:
            return None

        if record.addressline6 in [
            # split
            "B61 0NX",
            "B61 7AY",
            "B45 8HY",
            "B60 3AZ",
        ]:
            return None

        return super().address_record_to_dict(record)
