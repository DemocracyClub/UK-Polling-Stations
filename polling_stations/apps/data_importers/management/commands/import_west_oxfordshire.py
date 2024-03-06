from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "WOX"
    addresses_name = (
        "2024-05-02/2024-03-06T11:23:22.326044/Democracy_Club__02May2024.tsv"
    )
    stations_name = (
        "2024-05-02/2024-03-06T11:23:22.326044/Democracy_Club__02May2024.tsv"
    )
    elections = ["2024-05-02"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10093354712",  # CROFTERS BARN, HIRONS HILL, LITTLE ROLLRIGHT, CHIPPING NORTON
            "10033224093",  # BREW HOUSE COTTAGE CHASTLETON HOUSE ROAD THROUGH CHASTLETON, CHASTLETON
            "10093354541",  # BARN CONVERSION BLISS FARM CHURCHILL ROAD, CHIPPING NORTON
            "10093355282",  # BOULTERS GRANGE, CHURCHILL ROAD, CHIPPING NORTON
            "100120970316",  # SUNNYCROFT, BURFORD ROAD, MINSTER LOVELL, WITNEY
            "10024177121",  # 1 TIMBER YARD, BRADWELL GROVE, BURFORD
            "10024177122",  # 2 TIMBER YARD, BRADWELL GROVE, BURFORD
            "10024177123",  # 3 TIMBER YARD, BRADWELL GROVE, BURFORD
        ]:
            return None

        if record.addressline6 in [
            # split
            "OX20 1RZ",
            "OX18 1PU",
            "OX28 6DH",
            "OX18 3NU",
            "OX7 4BJ",
            # suspect
            "OX7 6UQ",
            "OX7 6WJ",
            "OX18 1PS",
            "OX7 6HX",
        ]:
            return None

        return super().address_record_to_dict(record)
