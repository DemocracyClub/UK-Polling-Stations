from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "MTY"
    addresses_name = "2024-07-04/2024-06-08T12:05:23.815608/Eros_SQL_Output005.csv"
    stations_name = "2024-07-04/2024-06-08T12:05:23.815608/Eros_SQL_Output005.csv"
    elections = ["2024-07-04"]

    def station_record_to_dict(self, record):
        # PONTSTICILL MEMORIAL HALL, CF48 2UR
        if record.pollingstationnumber == "54":
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
        if record.housepostcode in [
            "CF48 1TL",  # split
        ]:
            return None

        return super().address_record_to_dict(record)
