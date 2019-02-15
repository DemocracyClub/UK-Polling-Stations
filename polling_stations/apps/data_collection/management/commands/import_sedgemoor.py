from data_collection.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "E07000188"
    addresses_name = (
        "local.2019-05-02/Version 2/polling_station_export sedgemoor-2019-02-07.csv"
    )
    stations_name = (
        "local.2019-05-02/Version 2/polling_station_export sedgemoor-2019-02-07.csv"
    )
    elections = ["local.2019-05-02"]

    def address_record_to_dict(self, record):

        if record.housepostcode == "TA2 8PQ":
            rec = super().address_record_to_dict(record)
            rec["postcode"] = "TA2 8RQ"
            return rec

        if record.housepostcode == "TA7 0SB":
            rec = super().address_record_to_dict(record)
            rec["postcode"] = "TA7 0SD"
            return rec

        if record.housepostcode == "TA5 1QS":
            rec = super().address_record_to_dict(record)
            rec["postcode"] = "TA5 2QS"
            return rec

        if record.housepostcode == "BS26 2XA":
            rec = super().address_record_to_dict(record)
            rec["postcode"] = "BS26 2HU"
            return rec

        if record.uprn == "10023413245":
            rec = super().address_record_to_dict(record)
            rec["postcode"] = "TA5 2FR"
            return rec

        if record.uprn == "10009317377":
            rec = super().address_record_to_dict(record)
            rec["postcode"] = "TA6 7QH"
            return rec

        return super().address_record_to_dict(record)
