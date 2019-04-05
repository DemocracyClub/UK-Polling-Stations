from data_collection.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "E07000029"
    addresses_name = (
        "local.2019-05-02/Version 1/polling_station_export-2019-03-19cope.csv"
    )
    stations_name = (
        "local.2019-05-02/Version 1/polling_station_export-2019-03-19cope.csv"
    )
    elections = ["local.2019-05-02"]

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.uprn.strip().lstrip("0")

        if record.houseid == "7000048":
            rec["postcode"] = "CA27 0AT"

        if record.housepostcode == "CA20 1EX":
            return None

        if uprn in [
            "10000896294",  # CA191XR -> CA191XG : Whitegarth, Drigg, Holmrook, Cumbria
            "10000893985",  # CA191UU -> CA191TJ : Birkerthwaite, Birker Moor, Eskdale Green, Eskdale, Cumbria
            "100110689644",  # LA195UR -> LA195UD : Shannon Rise, Summer Hill, Bootle, Millom, Cumbria
            "10000892777",  # LA195YJ -> LA195YH : Thornycroft, Waberthwaite, Millom, Cumbria
            "10000903207",  # CA286DA -> CA286DL : 2 Omega Court, New Road, Whitehaven, Cumbria
        ]:
            rec["accept_suggestion"] = True

        if uprn in [
            "10000896318",  # CA191XD -> CA191XE : Sandford, Drigg, Holmrook, Cumbria
            "100110311815",  # LA184DE -> LA184DG : 49 Wellington Street, Millom, Cumbria
            "10000903848",  # CA201QG -> CA255LA : 5 The Bridles, Seascale, Cumbria
            "10000896234",  # CA222UR -> CA222UP : Primrose Bank, Coulderton, Egremont, Cumbria
            "10000897219",  # LA195UP -> LA195UR : Moor Green, Whitbeck, Millom, Cumbria
            "10000891448",  # CA263XG -> CA263XF : Tile Kiln, Arlecdon Park Road, Arlecdon, Frizington, Cumbria
            "100110798223",  # CA287AY -> CA287AQ : Flat 2, St Nicholas Chambers, Church Street, Whitehaven, Cumbria
            "100110735446",  # CA287AY -> CA287AQ : Flat 1, St Nicholas Chambers, Church Street, Whitehaven, Cumbria
            "10000907596",  # CA255JD -> CA263XS : Squirrels Nook, Birks Road, Cleator Moor, Cumbria
            "10000904699",  # CA145UJ -> LA184EY : 3 Globe Terrace, Main Street, Distington, Workington, Cumbria
            "10000907460",  # LA184GY -> CA144SH : 14 Timberwood Close, Haverigg, Millom, Cumbria
        ]:
            rec["accept_suggestion"] = False

        return rec
