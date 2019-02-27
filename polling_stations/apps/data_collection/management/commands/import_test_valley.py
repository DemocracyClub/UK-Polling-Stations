from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000093"
    addresses_name = "local.2019-05-02/Version 1/Democracy_Club__02May2019test.tsv"
    stations_name = "local.2019-05-02/Version 1/Democracy_Club__02May2019test.tsv"
    elections = ["local.2019-05-02"]
    csv_delimiter = "\t"
    csv_encoding = "windows-1252"

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if record.addressline6 == "S051 0JQ":
            rec["postcode"] = "SO51 0JH"

        if uprn in [
            "200010018966",  # SO206AZ -> SO206AX : The Mayfly, Testcombe, Wherwell, Andover, Hampshire
            "200000723154",  # SO208DP -> SO208DR : The Lodge, Garlogs, Nine Mile Water, Nether Wallop, Stockbridge, Hampshire
            "200000714047",  # SO208DT -> SO208EG : Lark Rise, Romsey Road, Nether Wallop, Stockbridge, Hampshire
            "200010012330",  # SO208EG -> SO208HN : The Old George, Salisbury Road, Middle Wallop, Stockbridge, Hampshire
            "200010018935",  # SP102LH -> SP102JN : Anton Arms, Salisbury Road, Andover, Hampshire
            "200010013598",  # SP117EY -> SP117EB : Walnut Tree Cottage, Streetway Road, Grateley, Andover, Hampshire
            "200010019045",  # SP102EF -> SP102EG : The Southampton Arms, Winchester Street, Andover, Hampshire
            "200010011351",  # SP117QY -> SP117QX : Glenrosa, Yew Tree Farm, Village Street, Goodworth Clatford, Andover, Hampshire
            "200000712964",  # SP117QX -> SP117QZ : 1 Laurel Cottages, Village Street, Goodworth Clatford, Andover, Hampshire
            "200000722553",  # SP118PX -> SP118PU : 1 Lains Paddock, Lains Farm, Cholderton Road, Quarley, Andover, Hampshire
            "200010018117",  # SP118AP -> SP118AN : Annex at Bryning Lodge, Green Lane, Monxton, Andover, Hampshire
            "200000709654",  # SO510HE -> SO510HS : 1 New Cottages, Awbridge Hill, Awbridge, Romsey, Hampshire
            "200000706708",  # SO510HE -> SO510HS : 2 New Cottages, Awbridge Hill, Awbridge, Romsey, Hampshire
            "200000713285",  # SP118PX -> SP118PH : Kimpton Cottage, The Green, Kimpton, Andover, Hampshire
            "200000715087",  # SP40EE -> SP40DR : 55 Spinney Cottage, Cholderton, Salisbury, Wiltshire
            "200010018694",  # SO516EQ -> SO516DX : Strawberry Cottage, Shorts Farm, Scallows Lane, Wellow, Romsey, Hampshire
            "200000717175",  # SO516FS -> SO516ZR : Workshop Flat, St Edwards Sch, Melchet Court, Plaitford, Romsey, Hampshire
            "100062537012",  # SO516EB -> SO516EA : 5 Bridge Cottages, Foxes Lane, Wellow, Romsey, Hampshire
            "100062537013",  # SO516EB -> SO516EA : 6 Bridge Cottages, Foxes Lane, Wellow, Romsey, Hampshire
            "200000708571",  # SO516FF -> SO516FD : Dunwood Manor Nursing Home, Salisbury Road, Sherfield English, Romsey, Hampshire
            "200000713728",  # SO510LE -> SO510LB : The Willows, Kimbridge Corner, Kimbridge, Michelmersh, Romsey, Hampshire
            "200000704203",  # SO510LU -> SO510LW : 1 Home Farm Flats, East Tytherley Road, Lockerley, Romsey, Hampshire
            "200000704204",  # SO510LU -> SO510LW : 2 Home Farm Flats, East Tytherley Road, Lockerley, Romsey, Hampshire
            "200000704205",  # SO510LU -> SO510LW : 3 Home Farm Flats, East Tytherley Road, Lockerley, Romsey, Hampshire
            "200000723659",  # SO510LP -> SO510LN : Lower Lodge, Mottisfont Abbey, Mottisfont, Romsey, Hampshire
            "200010015638",  # SO510LP -> SO510LN : Tithe Barn, Mottisfont Village Road, Mottisfont, Romsey, Hampshire
            "100060584432",  # SO208HR -> SO208HP : Piccadilly Cottage, Station Road, Over Wallop, Stockbridge Hampshire
            "200010016895",  # SP118NU -> SP118NJ : Summer Cottage, Bush Farm Lane, Thruxton, Andover, Hampshire
        ]:
            rec["accept_suggestion"] = True

        if uprn in [
            "200000712580",  # SO206AB -> SO206AZ : Down End, Drove Road, Chilbolton, Stockbridge, Hampshire
            "200000712580",  # SO206AB -> SO206AZ : Down End, Drove Road, Chilbolton, Stockbridge, Hampshire
            "100062540094",  # SO208QB -> SP103EL : 2 The Avenue, Middle Wallop, Stockbridge, Hampshire
            "100062539681",  # SO519AL -> SP102EG : 2 Winchester Road, Crampmoor, Romsey, Hampshire
            "200010015207",  # SP11 6JH -> SP118PW : 4 Woodhouse Smannell, Andover   Hampshire
        ]:
            rec["accept_suggestion"] = False

        return rec
