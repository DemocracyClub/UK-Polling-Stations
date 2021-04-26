from data_importers.management.commands import BaseXpressWebLookupCsvImporter


class Command(BaseXpressWebLookupCsvImporter):
    council_id = "HIN"
    addresses_name = "2021-04-16T11:29:13.327047/PropertyPostCodePollingStationWebLookup-2021-04-09.CSV"
    stations_name = "2021-04-16T11:29:13.327047/PropertyPostCodePollingStationWebLookup-2021-04-09.CSV"
    elections = ["2021-05-06"]
    csv_delimiter = ","

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "10033831876",  # THE STABLES, DESFORD LANE, RATBY, LEICESTER
            "100030520613",  # WOODCOCK), BROCKEY FARM, KIRKBY ROAD, BARWELL, LEICESTER
            "100030520609",  # BROCKEY FARM KIRKBY ROAD, BARWELL
            "10033728621",  # BARWELL SPORTS BAR, KIRKBY ROAD, BARWELL, LEICESTER
            "200002769579",  # START FARM, WATLING STREET, HINCKLEY
            "10033728228",  # KATES EQUESTRIAN SUPPLIES, 18 NEWTON ROAD, HINCKLEY
            "100030503769",  # 10 HILL STREET, BARWELL
        ]:
            return None

        if record.postcode in ["LE10 0QL", "LE9 8JA", "LE10 2GJ"]:
            return None

        return super().address_record_to_dict(record)
