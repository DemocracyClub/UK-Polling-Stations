from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "DER"
    addresses_name = "2021-03-12T15:52:38.494809/Democracy_Club__06May2021.tsv"
    stations_name = "2021-03-12T15:52:38.494809/Democracy_Club__06May2021.tsv"
    elections = ["2021-05-06"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "200001135441",  # FLAT THE HONEYCOMB LADYBANK ROAD, DERBY
            "10010685086",  # MORTGAGE FORCE LTD, 65A FRIAR GATE, DERBY
            "100030364800",  # 134 STATION ROAD, MICKLEOVER, DERBY
            "100030364798",  # 142 STATION ROAD, MICKLEOVER, DERBY
            "100030329310",  # FLAT 631 HARVEY ROAD, DERBY
            "100030361764",  # 68 TADDINGTON ROAD, CHADDESDEN, DERBY
            "100030361769",  # 66 TADDINGTON ROAD, CHADDESDEN, DERBY
            "10010614113",  # STONE FARM, SINFIN MOOR, DERBY
            "10010623517",  # EDALE HOUSE ROYAL SCHOOL FOR THE DEAF 180 ASHBOURNE ROAD, DERBY
        ]:
            return None

        if record.addressline6 in [
            "DE23 6AR",
            "DE1 1RX",
            "DE1 3NZ",
            "DE24 0LU",
            "DE21 4HF",
            "DE22 3FZ",
        ]:
            return None

        return super().address_record_to_dict(record)
