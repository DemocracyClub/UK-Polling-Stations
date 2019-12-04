from data_collection.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "E07000167"
    addresses_name = (
        "parl.2019-12-12/Version 1/polling_station_export-2019-11-19rye.csv"
    )
    stations_name = "parl.2019-12-12/Version 1/polling_station_export-2019-11-19rye.csv"
    elections = ["parl.2019-12-12"]
    allow_station_point_from_postcode = False

    def address_record_to_dict(self, record):

        if record.houseid == "2001336":
            rec = super().address_record_to_dict(record)
            rec["postcode"] = "YO61 4AY"
            return rec

        if record.houseid == "2004865":
            rec = super().address_record_to_dict(record)
            rec["postcode"] = "YO25 3XZ"
            return rec

        if record.houseid in ["2019306", "2019299"]:
            rec = super().address_record_to_dict(record)
            rec["postcode"] = "YO60 6SF"
            return rec

        if record.housepostcode == "YO6O 7JU":
            rec = super().address_record_to_dict(record)
            rec["postcode"] = "YO60 7JU"
            return rec

        if record.housepostcode == "YO17 9L7":
            rec = super().address_record_to_dict(record)

            rec["postcode"] = "YO17 9LU"
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

        if record.housepostcode == "YO17 8DG":
            return None

        if record.houseid == "6000115":
            rec = super().address_record_to_dict(record)
            rec["postcode"] = "YO62 5JA"
            return rec

        return super().address_record_to_dict(record)
