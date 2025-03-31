from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "AMB"
    addresses_name = (
        "2025-05-01/2025-03-05T12:10:33.836869/Democracy Club - Polling Districts.csv"
    )
    stations_name = (
        "2025-05-01/2025-03-05T12:10:33.836869/Democracy Club - Polling Stations.csv"
    )
    elections = ["2025-05-01"]
    csv_encoding = "utf-16le"

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")
        if uprn in [
            "100030011186",  # 50 BAKERS HILL, HEAGE, BELPER
        ]:
            return None

        if record.postcode in [
            # splits
            "DE75 7WF",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # council coord correction for: SOMERCOTES PARISH HALL Nottingham Road Somercotes Alfreton Derbyshire DE55 4LY
        if record.stationcode in [
            "75",
            "4",
        ]:
            record = record._replace(xordinate="442409", yordinate="353784")

        # corrections from council for the following stations:
        # TESCO SUPERSTORE, 24 Admiral Close, Heanor, DE75 7QH
        if record.stationcode == "29":
            record = record._replace(
                add1="High Street",
                postcode="DE75 7EX",
                xordinate="443032",
                yordinate="346571",
            )
        # WILMOT STREET CENTRE, 15 The Ropewalk, Heanor, DE75 7BL
        if record.stationcode == "27":
            record = record._replace(
                add1="Wilmot Street",
                postcode="DE75 7EF",
                xordinate="443402",
                yordinate="346258",
            )

        return super().station_record_to_dict(record)
