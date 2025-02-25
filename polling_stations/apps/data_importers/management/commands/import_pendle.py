from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "PEN"
    addresses_name = (
        "2025-05-01/2025-02-25T14:26:26.747567/Democracy_Club__01May2025.tsv"
    )
    stations_name = (
        "2025-05-01/2025-02-25T14:26:26.747567/Democracy_Club__01May2025.tsv"
    )
    elections = ["2025-05-01"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10022950288",  # PEARL COTTAGE, ALMA ROAD, COLNE
            "61014294",  # 117 EDWARD STREET, NELSON
            "100012398597",  # PLANTATION COTTAGE, GREENHEAD LANE, FENCE, BURNLEY
            "10024181464",  # FOSTERS LEAP BARN, TRAWDEN, COLNE
            "10024181048",  # WHITEMOOR BOTTOM FARM, WHITEMOOR ROAD, FOULRIDGE, COLNE
            "100012400306",  # BROWN HOUSE FARM, GISBURN OLD ROAD, BLACKO, NELSON
        ]:
            return None

        if record.addressline6 in [
            # suspect
            "BB9 7YS",
        ]:
            return None

        return super().address_record_to_dict(record)
