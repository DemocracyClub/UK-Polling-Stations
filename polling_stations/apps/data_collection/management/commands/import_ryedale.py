from data_collection.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "E07000167"
    addresses_name = "europarl.2019-05-23/Version 1/Ryedale District Council_polling_station_export-2019-05-09.csv"
    stations_name = "europarl.2019-05-23/Version 1/Ryedale District Council_polling_station_export-2019-05-09.csv"
    elections = ["europarl.2019-05-23"]

    def address_record_to_dict(self, record):

        if record.houseid == "2001336":
            rec = super().address_record_to_dict(record)
            rec["postcode"] = "YO614AY"
            return rec

        if record.houseid == "2004865":
            rec = super().address_record_to_dict(record)
            rec["postcode"] = "YO25 3XZ"
            return rec

        if record.houseid == "2021693":
            rec = super().address_record_to_dict(record)
            rec["postcode"] = "YO25 3BU"
            return rec

        if record.houseid in ["2019306", "2019299", "2019300"]:
            rec = super().address_record_to_dict(record)
            rec["postcode"] = "YO60 6SF"
            return rec

        if record.housepostcode == "YO6O 7JU":
            rec = super().address_record_to_dict(record)
            rec["postcode"] = "YO60 7JU"
            return rec

        if record.housepostcode == "YO17 9LB":
            return None

        if record.houseid == "2020682":
            rec = super().address_record_to_dict(record)
            rec["postcode"] = "YO60 6PA"
            return rec

        if record.houseid == "2020417":
            rec = super().address_record_to_dict(record)
            rec["postcode"] = "YO60 6PE"
            return rec

        if record.housepostcode in ["YO62 4AY", "YO62 4AT"]:
            return None

        if record.houseid == "6000115":
            rec = super().address_record_to_dict(record)
            rec["postcode"] = "YO62 5JA"
            return rec

        return super().address_record_to_dict(record)
