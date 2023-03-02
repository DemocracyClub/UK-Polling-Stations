from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "SAL"
    addresses_name = (
        "2023-05-04/2023-03-02T17:12:56.253915/Democracy_Club__04May2023.tsv"
    )
    stations_name = (
        "2023-05-04/2023-03-02T17:12:56.253915/Democracy_Club__04May2023.tsv"
    )
    elections = ["2023-05-04"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "100081131978",  # PADDOCK VIEW, AYRES END LANE, CHILDWICKBURY, ST. ALBANS
            "100080863526",  # 2 ROSE WALK, ST. ALBANS
            "100080863527",  # 3 ROSE WALK, ST. ALBANS
            "100080863525",  # 1 ROSE WALK, ST. ALBANS
            "10024115888",  # FLAT AT ST ALBANS SCHOOL PAVILLION 162 HARPENDEN ROAD, ST ALBANS
            "200003633693",  # WOOD END, HATCHING GREEN, HARPENDEN
            "100081134635",  # PLAISTOWES FARM, NOKE LANE, ST. ALBANS
        ]:
            return None

        if record.addressline6 in [
            # splits
            "AL3 5PR",
            "AL4 0TP",
            "AL4 0TG",
            "AL3 5PD",
        ]:
            return None

        return super().address_record_to_dict(record)
