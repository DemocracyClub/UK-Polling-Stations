from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "BDF"
    addresses_name = "2024-05-02/2024-02-27T11:59:39.691210/Pollling Districts.csv"
    stations_name = "2024-05-02/2024-02-27T11:59:39.691210/Polling Stations.csv"
    elections = ["2024-05-02"]
    csv_encoding = "utf-16le"

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "10093200695",  # WESTWOOD HOUSE, MELCHBOURNE ROAD, RISELEY, BEDFORD
            "200001852434",  # DEAN FARM, COLESDEN ROAD, COLMWORTH, BEDFORD
            "100080997913",  # CUCKOO BROOK HOUSE, ST. NEOTS ROAD, RENHOLD, BEDFORD
            "10002964874",  # HIGHFIELD HOUSE, GRAZE HILL LANE, RAVENSDEN, BEDFORD
            "100081214315",  # COWBRIDGE COTTAGE, AMPTHILL ROAD, KEMPSTON HARDWICK, BEDFORD
            "10090878428",  # THE GABLES, FALCON AVENUE, BEDFORD
            "100080013586",  # 50 FALCON AVENUE, BEDFORD
            "100080013584",  # 48 FALCON AVENUE, BEDFORD
            "100081209336",  # 140 CLAPHAM ROAD, CLAPHAM, BEDFORD
            "100081206809",  # TEMPLERS, 117A MIDLAND ROAD, BEDFORD
            "100080998897",  # SAILORS BRIDGE COTTAGE WOBURN ROAD, KEMPSTON
            "10090878776",  # WOLD FARM AIRFIELD ROAD, PODINGTON
            "10002972330",  # SUNCREST WESTFIELD ROAD, OAKLEY
            "10002975508",  # DUNGEE FARM, DUNGEE ROAD, ODELL, BEDFORD
            "100081209997",  # CLASSIC FURNITURE, 1A LONDON ROAD, BEDFORD
        ]:
            return None

        if record.postcode in [
            # splits
            "MK43 9BD",
            # looks wrong
            "MK45 3JE",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # KEMPSTON RURAL PRIMARY SCHOOL, MARTELL DRIVE, KEMPSTON, BEDFORD, MK42 7FJ
        if record.pollingstationid in ["12202", "12203"]:
            record = record._replace(xordinate="")
            record = record._replace(yordinate="")

        # WOOTTON COMMUNITY CENTRE ,HARRIS WAY ,WOOTTON, BEDFORD, MK43 9FZ
        if record.pollingstationid in ["12259", "12260", "12261"]:
            record = record._replace(xordinate="")
            record = record._replace(yordinate="")

        # CHURCH HALL, ST MARKS CHURCH, CALDER RISE, BEDFORD, MK41 7UY
        if record.pollingstationid in ["12291", "12292", "12290"]:
            record = record._replace(xordinate="")
            record = record._replace(yordinate="")

        # BEDFORD HOSPITAL, BEDFORD HOSPITAL, KEMPSTON ROAD, BEDFORD, MK42 9DJ
        if record.pollingstationid == "12234":
            record = record._replace(xordinate="")
            record = record._replace(yordinate="")

        # SPRINGFIELD SCHOOL, ORCHARD STREET, KEMPSTON, BEDFORD, MK42 7LJ
        if record.pollingstationid in ["12199", "12200"]:
            record = record._replace(xordinate="")
            record = record._replace(yordinate="")

        return super().station_record_to_dict(record)
