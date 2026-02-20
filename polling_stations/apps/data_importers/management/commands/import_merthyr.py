from data_importers.management.commands import BaseHalarose2026UpdateCsvImporter


class Command(BaseHalarose2026UpdateCsvImporter):
    council_id = "MTY"
    addresses_name = "2026-05-07/2026-02-20T15:14:47.599472/Democracy Club - Idox_2026-02-20 15-05.csv"
    stations_name = "2026-05-07/2026-02-20T15:14:47.599472/Democracy Club - Idox_2026-02-20 15-05.csv"
    elections = ["2026-05-07"]

    def station_record_to_dict(self, record):
        # PONTSTICILL MEMORIAL HALL, CF48 2UR
        if record.pollingstationnumber == "255":
            record = record._replace(pollingstationpostcode="CF48 2UD")
        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")
        if uprn in [
            "10034658436",  # TRIGG BROS, TY-NEWYDD FARM, TRELEWIS, TREHARRIS
            "200001851107",  # TYN-Y-COEDCAE FARM, SWANSEA ROAD, MERTHYR TYDFIL
            "200001639936",  # GAVENNY VILLA, HIGH STREET, PENYDARREN, MERTHYR TYDFIL
            "10034663931",  # HIGH GARDEN, TRAMROAD SIDE SOUTH, MERTHYR TYDFIL
        ]:
            return None
        if record.postcode in [
            "CF48 1TL",  # split
        ]:
            return None

        return super().address_record_to_dict(record)
