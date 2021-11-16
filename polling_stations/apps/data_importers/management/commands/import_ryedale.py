from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "RYE"
    addresses_name = (
        "2021-11-08T12:14:12.775016/RYEDALE_polling_station_export-2021-11-03.csv"
    )
    stations_name = (
        "2021-11-08T12:14:12.775016/RYEDALE_polling_station_export-2021-11-03.csv"
    )
    elections = ["2021-11-25"]

    def address_record_to_dict(self, record):
        if record.housepostcode in [
            "YO62 6PE",
            "YO17 9RL",
            "YO17 9LB",
            "YO60 7HQ",
            "YO41 1JF",
            "YO60 7NB",
            "YO62 6JA",
            "YO17 8AD",
            "YO17 9QY",
            "YO13 9PT",
            "YO18 7UE",
            "YO17 6BU",
            "YO17 6BW",
            "YO17 6BX",
        ]:
            return None

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
