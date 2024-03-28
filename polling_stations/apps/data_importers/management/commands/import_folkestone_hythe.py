from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "SHE"
    addresses_name = "2024-05-02/2024-02-29T10:38:45.624345/Polling Districts.csv"
    stations_name = "2024-05-02/2024-02-29T10:38:45.624345/Polling Stations.csv"
    elections = ["2024-05-02"]
    csv_encoding = "utf-16le"

    def address_record_to_dict(self, record):
        if record.postcode in [
            # split
            "TN29 9AU",
            "TN28 8PW",
            "CT20 3RE",
        ]:
            return None
        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # Amendment from council:
        # Old: Hawkinge Pavillion and Sports Ground, Pavillion Road, Hawkinge, Kent CT18 7AY
        # New: Hawkinge Pavilion and Sports Ground, Pavilion Road, Hawkinge, Kent, CT18 7UA
        if record.stationcode == "28":
            record = record._replace(
                xordinate="621844",
                yordinate="140818",
                postcode="CT18 7UA",
                placename="Hawkinge Pavilion and Sports Ground",
                add1="Pavilion Road",
            )
        # 1st Lyminge Scout Hut, Woodland Road, Lyminge, Kent CT18 8EW
        if record.stationcode == "42":
            record = record._replace(xordinate="615894", yordinate="140864")
        # Pembroke Court, Dover Road, Folkestone, CT20 1TA
        if record.stationcode == "15":
            record = record._replace(xordinate="623254", yordinate="136698")
        # New Romney Methodist Church Hall, High Street, New Romney, Kent, TN28 8AH
        if record.stationcode == "26":
            record = record._replace(xordinate="606553", yordinate="124860")
        # New Romney Methodist Church Hall, High Street, New Romney, Kent, TN28 8AH
        if record.stationcode == "26":
            record = record._replace(xordinate="606553", yordinate="124860")
        # Hawkinge Cricket Club, Cricketers Close, Hawkinge, Folkestone, CT18 7NH
        if record.stationcode == "27":
            record = record._replace(xordinate="621904", yordinate="140713")
        # Hawkinge Community Centre, Heron Forstal Avenue, Hawkinge, Folkestone, Kent, CT18 7FP
        if record.stationcode in [
            "29",
            "30",
        ]:
            record = record._replace(xordinate="621563", yordinate="139795")
        # Stelling Minnis Village Hall, Bossingham Road, Stelling Minnis, Kent, CT4 6AG
        if record.stationcode == "41":
            record = record._replace(xordinate="614748", yordinate="146625")
        # Rose and Crown, Swamp Road, Old Romney, Romney Marsh, Kent, TN29 9SQ
        if record.stationcode == "55":
            record = record._replace(xordinate="603097", yordinate="125105")
        # Brookland Village Hall, Boarmans Lane, Brookland, Kent, TN29 9QZ
        if record.stationcode == "57":
            record = record._replace(xordinate="598840", yordinate="125772")

        return super().station_record_to_dict(record)
