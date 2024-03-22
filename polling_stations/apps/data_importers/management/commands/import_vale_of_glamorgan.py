from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "VGL"
    addresses_name = (
        "2024-05-02/2024-03-22T16:08:51.555473/Democracy Club Polling Districts.csv"
    )
    stations_name = (
        "2024-05-02/2024-03-22T16:08:51.555473/Democracy Club Polling Stations.csv"
    )
    elections = ["2024-05-02"]
    csv_encoding = "utf-16le"

    def station_record_to_dict(self, record):
        # ROMILLY BOWLING CLUB, ROMILLY PARK ROAD, BARRY, VALE OF GLAMORGAN CF62 6RB
        if (record.stationcode, record.placename) == ("2", "ROMILLY BOWLING CLUB"):
            record = record._replace(postcode="")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")
        if uprn in [
            "64105362",  # FLAT GLAMORGANSHIRE GOLF CLUB LAVERNOCK ROAD, PENARTH
            "64116062",  # FIVE ACRES, ST. HILARY, COWBRIDGE
        ]:
            return None

        if record.postcode in [
            "CF62 6BA",  # split
            "CF71 7PY",  # suspect
        ]:
            return None
        return super().address_record_to_dict(record)
