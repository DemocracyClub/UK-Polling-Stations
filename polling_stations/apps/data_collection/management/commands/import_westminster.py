from data_collection.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "E09000033"
    addresses_name = (
        "local.2018-05-03/Version 1/polling_station_export-2018-03-20 Westminster.csv"
    )
    stations_name = (
        "local.2018-05-03/Version 1/polling_station_export-2018-03-20 Westminster.csv"
    )
    elections = ["local.2018-05-03"]

    def station_record_to_dict(self, record):

        # Spelling errors in original data
        if record.pollingstationnumber == "68":
            record = record._replace(pollingstationaddress_1="Broadbent Room")
        if record.pollingstationnumber == "81":
            record = record._replace(pollingstationaddress_2="Alderney Street")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):

        if record.housepostcode == "SW1P 4FF":
            return None

        if record.housepostcode == "SW11 1DB":
            return None

        if record.uprn == "100023479764":
            return None

        if record.uprn == "10033574601":
            return None

        if record.housepostcode == "SE1P 4SA":
            return None

        if record.houseid == "10010188" or record.houseid == "3114346":
            rec = super().address_record_to_dict(record)
            rec["postcode"] = "W1S 1NH"
            return rec

        if record.uprn == "10033633050":
            rec = super().address_record_to_dict(record)
            rec["postcode"] = "W2 3JT"
            return rec

        if record.houseid == "10007854":
            rec = super().address_record_to_dict(record)
            rec["postcode"] = "NW1 6DS"
            return rec

        if record.uprn == "10033555281":
            return None

        if record.houseid == "10002115":
            rec = super().address_record_to_dict(record)
            rec["postcode"] = "SW1X 7LJ"
            return rec

        if record.houseid == "3007640":
            return None

        if record.houseid == "10004469":
            return None

        if record.houseid == "10009330":
            rec = super().address_record_to_dict(record)
            rec["postcode"] = "W9 3QF"
            return rec

        if record.houseid == "10007728":
            return None

        if record.housepostcode == "W2 6PD":
            return None

        if record.houseid == "10010095":
            rec = super().address_record_to_dict(record)
            rec["postcode"] = "W9 2DL"
            return rec

        return super().address_record_to_dict(record)
