from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "BRC"
    addresses_name = "2024-07-04/2024-05-23T17:49:18.668326/Eros_SQL_Output006.csv"
    stations_name = "2024-07-04/2024-05-23T17:49:18.668326/Eros_SQL_Output006.csv"
    elections = ["2024-07-04"]

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "10022826533",  # THE BUNGALOW OAKWOOD PARK KENNELS PEACOCK LANE, WOKINGHAM
            "200000332122",  # THRUMS, FOLIEJON PARK, WINKFIELD, WINDSOR
        ]:
            return None
        if record.housepostcode in [
            # split
            "SL5 8RY",
            "RG42 6BX",
        ]:
            return None
        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # 'Binfield Memorial Hall, Terrace Road South, Binfield, BRACKNELL, RG42 4DJ'
        if record.pollingvenueid == "3":
            record = record._replace(pollingstationpostcode="")

        return super().station_record_to_dict(record)
