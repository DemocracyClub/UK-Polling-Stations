from data_collection.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "E07000029"
    addresses_name = (
        "parl.2019-12-12/Version 1/polling_station_export-2019-11-14cope.csv"
    )
    stations_name = (
        "parl.2019-12-12/Version 1/polling_station_export-2019-11-14cope.csv"
    )
    elections = ["parl.2019-12-12"]
    allow_station_point_from_postcode = False

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.uprn.strip().lstrip("0")

        if uprn == "10000901653":
            rec["postcode"] = "CA27 0AT"

        if record.housepostcode in [
            "CA28 6AQ",
            "CA20 1EE",
        ]:
            return None

        if uprn in [
            "10000896294",  # CA191XR -> CA191XG : Whitegarth, Drigg, Holmrook, Cumbria
            "10000893985",  # CA191UU -> CA191TJ : Birkerthwaite, Birker Moor, Eskdale Green, Eskdale, Cumbria
            "100110689644",  # LA195UR -> LA195UD : Shannon Rise, Summer Hill, Bootle, Millom, Cumbria
        ]:
            rec["accept_suggestion"] = True

        if uprn in [
            "10000896318",  # CA191XD -> CA191XE : Sandford, Drigg, Holmrook, Cumbria
            "100110311815",  # LA184DE -> LA184DG : 49 Wellington Street, Millom, Cumbria
            "10000897219",  # LA195UP -> LA195UR : Moor Green, Whitbeck, Millom, Cumbria
            "10000891448",  # CA263XG -> CA263XF : Tile Kiln, Arlecdon Park Road, Arlecdon, Frizington, Cumbria
            "10000904699",  # CA145UJ -> LA184EY : 3 Globe Terrace, Main Street, Distington, Workington, Cumbria
        ]:
            rec["accept_suggestion"] = False

        return rec
