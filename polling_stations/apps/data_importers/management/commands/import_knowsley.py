from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "KWL"
    addresses_name = (
        "2024-07-04/2024-06-10T16:01:11.650798/Democracy_Club__04July2024 (16).tsv"
    )
    stations_name = (
        "2024-07-04/2024-06-10T16:01:11.650798/Democracy_Club__04July2024 (16).tsv"
    )
    elections = ["2024-07-04"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "40035578",  # 182 RIBBLERS LANE, LIVERPOOL
            "40035577",  # 180 RIBBLERS LANE, LIVERPOOL
            "40003719",  # 121 BEWLEY DRIVE, SOUTHDENE, KIRKBY
            "40036487",  # 134 ROUGHWOOD DRIVE, LIVERPOOL
            "40025501",  # FOREST HOUSE, LIVERPOOL ROAD, PRESCOT
            "40048270",  # 10 CHURCH STREET, PRESCOT
        ]:
            return None

        if record.addressline6 in [
            # splits
            "L36 5YR",
            "L34 1LP",
            "L35 1QN",
        ]:
            return None

        return super().address_record_to_dict(record)
