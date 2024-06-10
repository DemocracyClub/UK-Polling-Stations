from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "GLG"
    addresses_name = "2024-07-04/2024-06-10T12:22:22.251389/Eros_SQL_Output003.csv"
    stations_name = "2024-07-04/2024-06-10T12:22:22.251389/Eros_SQL_Output003.csv"
    elections = ["2024-07-04"]

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "906700541051",  # 25 HAWICK COURT, GLASGOW
            "906700541052",  # 27 HAWICK COURT, GLASGOW
            "906700531273",  # UNIT 508B 47 KYLE STREET, GLASGOW
            "906700531270",  # UNIT 507H 47 KYLE STREET, GLASGOW
            "906700496057",  # FLAT 0/1 18 GREAT GEORGE STREET, GLASGOW
        ]:
            return None

        if record.housepostcode in [
            # splits
            "G53 6UW",
            "G22 6RL",
            "G21 2LN",
            "G61 1QE",
            "G33 3SU",
            "G14 9HQ",
            "G52 1RZ",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        if "LINTHAUGH NURSERY" in record.pollingstationname:
            record = record._replace(
                pollingstationpostcode=record.pollingstationaddress_5
            )
            record = record._replace(pollingstationaddress_5="")

        if "ST MARGARETS PARISH CHURCH HALL" in record.pollingstationname:
            record = record._replace(pollingstationpostcode="")

        return super().station_record_to_dict(record)
