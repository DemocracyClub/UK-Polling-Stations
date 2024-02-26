from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "WLA"
    addresses_name = (
        "2024-05-02/2024-02-26T12:35:17.676089/Democracy_Club__02May2024.tsv"
    )
    stations_name = (
        "2024-05-02/2024-02-26T12:35:17.676089/Democracy_Club__02May2024.tsv"
    )
    elections = ["2024-05-02"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10012356569",  # 3 THE GRAVEL, MERE BROW, PRESTON
            "10012344947",  # 201 SHAW HALL CARAVAN PARK SMITHY LANE, SCARISBRICK
            "10012365587",  # FLAT 1, HEBA HOUSE, 4 AUGHTON STREET, ORMSKIRK
            "10012363964",  # 1 COLLIER WAY, UPHOLLAND, SKELMERSDALE
            "10012355457",  # APARTMENT 47, BROOKSIDE, AUGHTON STREET, ORMSKIRK
            "10012365587",  # FLAT 1, HEBA HOUSE, 4 AUGHTON STREET, ORMSKIRK
            "10012360939",  # 1 TOWER VIEW CLOSE, BURSCOUGH, ORMSKIRK
            "100012414181",  # ALTYS FARM, ALTYS LANE, ORMSKIRK
        ]:
            return None

        if record.addressline6 in [
            # split
            "WN8 7XA",
            "PR4 6RT",
            "PR9 8FB",
            "L40 5BE",
            "L39 8SR",
            "WN6 9QE",
            "L40 6JA",
            "WN6 9EN",
            "WN8 6SH",
        ]:
            return None

        return super().address_record_to_dict(record)
