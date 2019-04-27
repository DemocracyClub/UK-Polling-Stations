from data_collection.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "E07000061"
    addresses_name = (
        "local.2019-05-02/Version 1/polling_station_export-2019-02-26Eastb.csv"
    )
    stations_name = (
        "local.2019-05-02/Version 1/polling_station_export-2019-02-26Eastb.csv"
    )
    elections = ["local.2019-05-02", "europarl.2019-05-23"]

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "10010661279",  # BN208EJ -> BN207EJ : FLAT 6 8 CARLISLE ROAD, EASTBOURNE, EAST SUSSEX
            "10010663461",  # BN211HG -> BN211HH : THE LAMBE INN HIGH STREET, EASTBOURNE, EAST SUSSEX
        ]:
            rec["accept_suggestion"] = True

        if uprn in [
            "10024140467",  # BN213EU -> BN228AG : 143 / 145 LANGNEY ROAD, EASTBOURNE, EAST SUSSEX
            "100061919876",  # BN208NH -> BN208NR : THE DRIVE 153 VICTORIA DRIVE, EASTBOURNE, EAST SUSSEX
        ]:
            rec["accept_suggestion"] = False

        return rec
