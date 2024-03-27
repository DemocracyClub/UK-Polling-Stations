from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "MTY"
    addresses_name = "2024-05-02/2024-03-27T11:39:56.682597/Eros_SQL_Output004.csv"
    stations_name = "2024-05-02/2024-03-27T11:39:56.682597/Eros_SQL_Output004.csv"
    elections = ["2024-05-02"]

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
        ]:
            return None
        if record.housepostcode in [
            "CF48 1TL",  # split
        ]:
            return None

        return super().address_record_to_dict(record)
