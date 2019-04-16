from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000028"
    addresses_name = "local.2019-05-02/Version 1/Democracy_Club__02May2019Car.tsv"
    stations_name = "local.2019-05-02/Version 1/Democracy_Club__02May2019Car.tsv"
    elections = ["local.2019-05-02"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "100110688054",  # CA27LS -> CA27LL : Flat 1 Coledale Hall, Newtown Road, Carlisle
            "100110688055",  # CA27LS -> CA27LL : Flat 2 Coledale Hall, Newtown Road, Carlisle
            "100110688056",  # CA27LS -> CA27LL : Flat 3 Coledale Hall, Newtown Road, Carlisle
            "100110688057",  # CA27LS -> CA27LL : Flat 4 Coledale Hall, Newtown Road, Carlisle
            "100110688058",  # CA27LS -> CA27LL : Flat 5 Coledale Hall, Newtown Road, Carlisle
            "10009456571",  # CA64ND -> CA64HS : 24 Harker Park, Carlisle
        ]:
            rec["accept_suggestion"] = True

        if uprn in [
            "100110727990",  # CA39LJ -> CA12JQ : 12 Bowscale Close, Carlisle
            "100110727992",  # CA39LJ -> CA12JQ : 14 Bowscale Close, Carlisle
            "100110727993",  # CA39LJ -> CA12JQ : 15 Bowscale Close, Carlisle
            "100110727994",  # CA39LJ -> CA12JQ : 16 Bowscale Close, Carlisle
            "100110727995",  # CA39LJ -> CA12JQ : 17 Bowscale Close, Carlisle
            "100110727996",  # CA39LJ -> CA12JQ : 19 Bowscale Close, Carlisle
            "100110727997",  # CA39LJ -> CA12JQ : 20 Bowscale Close, Carlisle
            "100110727998",  # CA39LJ -> CA12JQ : 21 Bowscale Close, Carlisle
            "10008690791",  # CA39LJ -> CA12HB : 22 Bowscale Close, Carlisle
            "100110728000",  # CA39LJ -> CA12JQ : 23 Bowscale Close, Carlisle
            "100110728001",  # CA39LJ -> CA12JQ : 24 Bowscale Close, Carlisle
            "100110281591",  # CA39LJ -> CA12JQ : 25 Bowscale Close, Carlisle
            "100110728003",  # CA39LJ -> CA12JQ : 26 Bowscale Close, Carlisle
            "100110281593",  # CA39LJ -> CA12JQ : 27 Bowscale Close, Carlisle
            "10009459500",  # CA65PG -> CA65PX : The Stable Glencroft, Longtown, Carlisle
            "10008703905",  # CA81AU -> CA65SJ : Glenesk, Greenfield Lane, Brampton, Cumbria
            "10008697933",  # CA81EB -> CA89HT : 29 Irthing Park, Brampton, Cumbria
            "10008684650",  # CA11HB -> CA11JX : Flat 2, 5 Chatsworth Square, Carlisle
            "10008683732",  # CA11HB -> CA11JX : Flat 3, 5 Chatsworth Square, Carlisle
            "10008704189",  # CA24TT -> CA30BT : 443 Durdar Road, Durdar, Carlisle
            "100110302060",  # CA27BL -> CA26HH : 23 Osborne Avenue, Carlisle
        ]:
            rec["accept_suggestion"] = False

        return rec
