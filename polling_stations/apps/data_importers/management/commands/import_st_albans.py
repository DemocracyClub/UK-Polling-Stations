from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "SAL"
    addresses_name = (
        "2024-07-04/2024-05-27T15:28:11.936187/Democracy_Club__04July2024.tsv"
    )
    stations_name = (
        "2024-07-04/2024-05-27T15:28:11.936187/Democracy_Club__04July2024.tsv"
    )
    elections = ["2024-07-04"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "100081131978",  # PADDOCK VIEW, AYRES END LANE, CHILDWICKBURY, ST. ALBANS
            "10024115888",  # FLAT AT ST ALBANS SCHOOL PAVILLION 162 HARPENDEN ROAD, ST ALBANS
            "200003633693",  # WOOD END, HATCHING GREEN, HARPENDEN
            "100081134635",  # PLAISTOWES FARM, NOKE LANE, ST. ALBANS
        ]:
            return None

        if record.addressline6 in [
            # splits
            "AL3 5PR",
            "AL4 0LD",
            "AL1 3NS",
            "AL4 0TP",
            "AL3 5PD",
            # suspect
            "AL5 1AB",
            "AL5 1AA",
            "AL1 5NT",
            "AL5 2AB",
        ]:
            return None

        return super().address_record_to_dict(record)
