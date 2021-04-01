from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "MEN"
    addresses_name = (
        "2021-03-22T10:35:38.602035/Mendip polling_station_export-2021-03-20.csv"
    )
    stations_name = (
        "2021-03-22T10:35:38.602035/Mendip polling_station_export-2021-03-20.csv"
    )
    elections = ["2021-05-06"]
    csv_delimiter = ","

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "250002342",  # 15 UNDERHILL CLOSE, STREET
            "250002337",  # 191B HIGH STREET, STREET
            "250045108",  # ORCHARD BYRE, POLSHAM, WELLS
            "250070118",  # NEW MANOR FARM, POLSHAM, WELLS
            "250011489",  # HONEYSUCKLE COTTAGE, HAVYATT, GLASTONBURY
            "250044905",  # SUGAR LOAF BARN, KEWARD, WELLS
            "250054828",  # THE HUNTERS, TADHILL, LEIGH UPON MENDIP, RADSTOCK
            "250062887",  # THE ANNEXE WITHAM HALL FARM WITHAM HALL FARM TO BUNNS LANE, WITHAM FRIARY, FROME
            "250030360",  # LILLEYS CIDER, ROEWOOD FARM ESTATE, BUNNS LANE, WEST WOODLANDS, FROME
            "250060445",  # RIVERSIDE, BUNNS LANE, WEST WOODLANDS, FROME
            "250072443",  # FROME MEDICAL CENTRE, ENOS WAY, FROME
            "250040297",  # LITTLE ORCHARD, RUDGE ROAD, STANDERWICK, FROME
            "250040299",  # MERRION, RUDGE ROAD, STANDERWICK, FROME
            "250038119",  # MILL COTTAGE, IRON MILL LANE, OLDFORD, FROME
            "250043259",  # 5 RED HOUSE HOLIDAY HOMES WHITE POST TO CHARLTON ROAD, STRATTON ON THE FOSSE, SHEPTON MALLET
            "250040953",  # MOUNT PLEASANT, CHILCOMPTON, RADSTOCK
        ]:
            return None

        if record.housepostcode in [
            "BA5 1RJ",
            "BA5 3QR",
            "BA6 9DH",
            "BA6 8DA",
            "BA6 8AP",
            "BA4 4BT",
            "BA4 4DP",
            "BA4 5HB",
            "BA3 4DN",
            "BA16 0BG",
            "BA16 0BD",
            "BA16 0JL",
            "BA16 0NU",
            "BA5 2FF",
            "BA11 2ED",
            "BA11 2AU",
            "BA11 2XG",
            "BA11 5EP",
            "BA11 2TQ",
            "BA11 4AJ",
            "BA11 4FJ",
            "BA11 5HA",
            "BA11 5BT",
            "BA3 5QE",
            "BA11 4NY",
            "BA16 0GJ",
            "BA6 8PE",
            "BA11 5FE",
            "BA5 3DS",
        ]:
            return None

        return super().address_record_to_dict(record)
