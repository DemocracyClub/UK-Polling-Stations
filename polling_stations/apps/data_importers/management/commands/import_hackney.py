from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "HCK"
    addresses_name = (
        "2024-05-02/2024-03-04T14:37:16.630995/Democracy_Club__02May2024.CSV"
    )
    stations_name = (
        "2024-05-02/2024-03-04T14:37:16.630995/Democracy_Club__02May2024.CSV"
    )
    elections = ["2024-05-02"]

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10008342758",  # 20 MILLFIELDS PARADE, MILLFIELDS ROAD, LONDON
            "10008354539",  # 22 MILLFIELDS PARADE, MILLFIELDS ROAD, LONDON
            "200001073528",  # POTTERY HOUSE, ELRINGTON ROAD, LONDON
            "10008340028",  # FLAT E, 112 KINGSLAND ROAD, LONDON
            "10008245689",  # SECOND FLOOR FLAT 126 KINGSLAND HIGH STREET, HACKNEY, LONDON
            "10008245688",  # FIRST FLOOR FLAT 126 KINGSLAND HIGH STREET, HACKNEY, LONDON
            "10008245690",  # THIRD FLOOR FLAT 126 KINGSLAND HIGH STREET, HACKNEY, LONDON
            "10008353260",  # 1A SHEPHERDESS WALK, LONDON
            "10008353261",  # 1C SHEPHERDESS WALK, LONDON
            "100023136742",  # 5 SHEPHERDESS WALK, LONDON
            "10008233474",  # 97 CHATSWORTH ROAD, LONDON
        ]:
            return None

        if record.addressline6 in [
            # split
            "N1 6RH",
            "E5 9UF",
            # suspect
            "N16 5TU",  # Stamford Hill, Manor Parade
        ]:
            return None
        return super().address_record_to_dict(record)
