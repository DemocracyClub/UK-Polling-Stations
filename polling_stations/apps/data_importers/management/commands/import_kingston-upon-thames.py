from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "KTT"
    addresses_name = "2026-05-07/2026-03-17T09:05:17.344225/RBK - Polling Districts.csv"
    stations_name = "2026-05-07/2026-03-17T09:05:17.344225/RBK - Polling Stations.csv"
    elections = ["2026-05-07"]
    csv_encoding = "utf-16le"

    def address_record_to_dict(self, record):
        if record.postcode in [
            "KT2 7DA",  # split
        ]:
            return None
        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # The following are stations amendments for the council:

        # Christ Church C Of E Primary School, Pine Garden, Surbiton
        if record.stationcode == "BRA-K_3":
            record = record._replace(xordinate="519309", yordinate="167339")

        # Temporary Station - Kings College Sports Ground, Windsor Avenue, New Malden
        if record.stationcode == "GLD-W_22":
            record = record._replace(xordinate="520201.89", yordinate="167894.86")

        # Temporary Station Norbiton Train Station, Coombe Road, Kingston Upon Thames
        if record.stationcode == "CHB-R_13":
            record = record._replace(xordinate="519450.08", yordinate="169539.84")

        # St Pius X Catholic Church, The Triangle, The Triangle, Kingston Upon Thames, Surrey
        if record.stationcode == "CVD-R_18":
            record = record._replace(placename="St Pius X Catholic Church")
        return super().station_record_to_dict(record)
