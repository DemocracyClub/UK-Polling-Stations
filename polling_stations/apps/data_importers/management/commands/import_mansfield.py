from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "MAS"
    addresses_name = "2021-03-17T14:10:56.004783/polling_station_export-2021-03-17.csv"
    stations_name = "2021-03-17T14:10:56.004783/polling_station_export-2021-03-17.csv"
    elections = ["2021-05-06"]
    csv_delimiter = ","

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "10091484435",  # 33B ALBERT STREET, MANSFIELD
            "100031427156",  # 207 WESTFIELD LANE, MANSFIELD
            "100031413924",  # FIRBANK HOUSE, NEWLANDS ROAD, FOREST TOWN, MANSFIELD
            "100031415038",  # GREENACRES, OAKFIELD LANE, WARSOP, MANSFIELD
            "10023932919",  # GLEADTHORPE GRANGE FARM NETHERFIELD LANE, MEDEN VALE
        ]:
            return None

        if record.housepostcode in [
            "NG19 6JF",
            "NG19 6AT",
            "NG18 5RT",
            "NG18 1EU",
            "NG18 1ER",
            "NG18 1EJ",
            "NG18 1BQ",
            "NG18 4LN",
        ]:
            return None

        return super().address_record_to_dict(record)
