from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "ERE"
    addresses_name = "2025-05-01/2025-03-06T13:02:10.485125/Eros_SQL_Output005.csv"
    stations_name = "2025-05-01/2025-03-06T13:02:10.485125/Eros_SQL_Output005.csv"
    elections = ["2025-05-01"]
    csv_encoding = "windows-1252"

    def address_record_to_dict(self, record):
        record.uprn.strip().lstrip("0")

        if record.uprn in [
            "100030142270",  # BARN END, CAT & FIDDLE LANE, WEST HALLAM, ILKESTON
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # Add missing postcode for PORTA CABIN, BOSWORTH WAY, LONG EATON
        if record.pollingstationnumber == "25":
            record = record._replace(pollingstationpostcode="NG10 1PL")

        if record.pollingstationnumber == "1":
            # Add missing postcode for ABBOTSFORD COMMUNITY CENTRE (THE POD)
            record = record._replace(pollingstationpostcode="DE7 9JJ")

        if record.pollingstationnumber == "5":
            # Add missing postcode for COTMANHAY PAVILION
            record = record._replace(pollingstationpostcode="DE7 8BN")

        if record.pollingstationnumber == "19":
            # Add missing postcode for TOWN HALL, LONG EATON
            record = record._replace(pollingstationpostcode="NG10 1HU")

        if record.pollingstationnumber == "14":
            # Add missing postcode for ILKESTON METHODIST CHURCH
            record = record._replace(pollingstationpostcode="DE7 8BD")

        if record.pollingstationnumber == "13":
            # Add missing postcode for TOWN HALL, ILKESTON MARKET PNLACE, ILKESTON
            record = record._replace(pollingstationpostcode="DE7 5RP")

        if record.pollingstationnumber == "3":
            # Add missing postcode for CHRIST CHURCH COTMANHAY, VICARAGE STREET, ILKESTON, DERBYSHIRE
            record = record._replace(pollingstationpostcode="DE7 8QL")

        return super().station_record_to_dict(record)
