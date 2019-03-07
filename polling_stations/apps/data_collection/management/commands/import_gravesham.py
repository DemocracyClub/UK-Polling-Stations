from data_collection.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "E07000109"
    addresses_name = (
        "local.2019-05-02/Version 1/polling_station_export-2019-02-28Grave.csv"
    )
    stations_name = (
        "local.2019-05-02/Version 1/polling_station_export-2019-02-28Grave.csv"
    )
    elections = ["local.2019-05-02"]
    csv_encoding = "windows-1252"

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.uprn.strip().lstrip("0")

        if record.pollingstationnumber == "n/a":
            return None

        if uprn in [
            "100060952511",  # DA123AR -> DA123AY : Burleigh Sole Street Road, Cobham, Gravesend, Kent
            "10012014481",  # DA130XG -> DA130BS : Penlee Cottage Off Dean Lane, Luddesdown, Gravesend, Kent
        ]:
            rec["accept_suggestion"] = True

        if uprn in [
            "100060940357",  # DA118QT -> DA110JF : 71 Pelham Road South, Gravesend, Kent
            "10012025024",  # DA118BL -> DA118BJ : Wombwell Hall Nursing Home, Northfleet, Gravesend, Kent
            "100062313137",  # DA130QN -> DA130AA : South House Wrotham Road, Meopham, Gravesend, Kent
            "10012027211",  # DA122RE -> DA122BT : Flat Above 4-5 Milton Road, Gravesend, Kent
        ]:
            rec["accept_suggestion"] = False

        return rec
