from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "THR"
    addresses_name = (
        "2023-05-04/2023-04-19T13:00:54.850754/Democracy_Club__04May2023.tsv"
    )
    stations_name = (
        "2023-05-04/2023-04-19T13:00:54.850754/Democracy_Club__04May2023.tsv"
    )
    elections = ["2023-05-04"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10095907154",  # 1A HIGH STREET, GRAYS
            "200001553308",  # HILLVIEW, SOUTHEND ROAD, CORRINGHAM, STANFORD-LE-HOPE
            "100091297871",  # HOB HILL FARM, BIGGIN LANE, GRAYS
        ]:
            return None

        if record.addressline6.strip() in [
            # splits
            "RM19 1QJ",
            "RM16 4RB",
        ]:
            return None  # split

        return super().address_record_to_dict(record)
