from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000043"
    addresses_name = "parl.2019-12-12/Version 1/Democracy Club - Polling Station Data - North Devon Council.CSV"
    stations_name = "parl.2019-12-12/Version 1/Democracy Club - Polling Station Data - North Devon Council.CSV"
    elections = ["parl.2019-12-12"]
    allow_station_point_from_postcode = True

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10012095333",  # EX379AB -> EX379AR : Umberleigh Mill, Umberleigh, Devon
            "100040248151",  # EX313RB -> EX313RX : 4 Honeysuckle Close, Brynsworthy Park, Roundswell, Barnstaple, Devon
            "100040248148",  # EX313RB -> EX313RX : 1 Honeysuckle Close, Brynsworthy Park, Roundswell, Barnstaple, Devon
            "10091211100",  # EX314SG -> EX314NA : Annexe South Stowford Farm, Bratton Fleming, Barnstaple, Devon
            "100041137834",  # EX332JA -> EX332ES : 3 Butts Cottage, Chaloners Road, Braunton, North Devon
            "100040260168",  # EX331LG -> EX332LA : Springhaven, Pounds Meadow, Braunton, North Devon
            "10012111635",  # EX331HW -> EX331HN : Buckland Farmhouse, Buckland, Braunton, North Devon
            "10012114156",  # EX331HW -> EX331HN : Buckland Barton Cottage, Buckland, Braunton, North Devon
            "100040259238",  # EX331AA -> EX332ES : Flat 13, Cross Tree Centre, Braunton, North Devon
            "100040259239",  # EX331AA -> EX332ES : Flat, 14 Cross Tree Centre, Braunton, North Devon
            "100040259237",  # EX331AA -> EX332ES : Flat 12, Cross Tree Centre, Braunton, North Devon
            "100040259240",  # EX331AA -> EX332ES : Flat 15, Cross Tree Centre, Braunton, North Devon
            "100040259241",  # EX331AA -> EX332ES : Flat 16, Cross Tree Centre, Braunton, North Devon
            "100040259243",  # EX331AA -> EX332ES : Flat 18, Cross Tree Centre, Braunton, North Devon
            "100040259242",  # EX331AA -> EX332ES : Flat 17, Cross Tree Centre, Braunton, North Devon
            "100040259242",  # EX331AF -> EX332ES : 17 Sunny Nook, Cross Tree, Braunton, North Devon
            "100040261566",  # EX332AA -> EX332AF : 44 South Street, Braunton, Devon.
            "10012098448",  # EX379EF -> EX379ES : Millmoor Cottage, Burrington, Umberleigh, Devon
            "100040245337",  # EX327DL -> EX311EW : 11 Queen Anne`s Court Flats Castle Street, Barnstaple, Devon.
            "100041137194",  # EX328LU -> EX328LS : Flat 1 Above The Pet Shop, The Square, Barnstaple
            "100041137195",  # EX328LU -> EX328LS : Flat 2 Above The Pet Shop, The Square, Barnstaple
            "10012097723",  # EX187DU -> EX187JR : Stable Cottage, Beara Farm, Chulmleigh, Devon
            "10012097418",  # EX379ES -> EX379ET : Colleton Mill Cottage, Colleton Mills, Umberleigh, Devon
            "10000486684",  # EX340AN -> EX340AP : Seaspray, 2 Borough Road, Combe Martin, Ilfracombe, Devon
            "10012091238",  # EX340NF -> EX340NE : Glendale, Wood Lane, Combe Martin, Devon
            "10012102485",  # EX340AT -> EX340BB : Whitegates House, Woodlands, Combe Martin, Devon
            "10012090155",  # EX169JW -> EX363PE : Oak Cottage, East Anstey, Tiverton, Devon
            "100040249218",  # EX313XW -> EX313HW : 21 Littlemoor Close, West Yelland, Barnstaple
            "10012101625",  # EX394LE -> EX394LR : Robyns Patch Holmacott Cross, Holmacott, Instow, Bideford
            "10012090612",  # EX313PL -> EX313PB : Meadow View, Newton Tracey, Barnstaple, Devon
            "10012101587",  # EX349QF -> EX349QE : Flat B, 61/62 High Street, Ilfracombe, Devon
            "100040265196",  # EX349QF -> EX349QE : Flat A, 61/62 High Street, Ilfracombe, Devon
            "100040265157",  # EX349EZ -> EX349HE : Flat 5/6, 141 High Street, Ilfracombe, Devon
            "100040265549",  # EX349DA -> EX349NL : Flat 3 Portland Villas, Hostle Park Road, Hostle Park Road, Ilfracombe, Devon
            "100040265547",  # EX349DA -> EX349NL : Flat 1 Portland Villas, Hostle Park Road, Hostle Park Road, Ilfracombe, Devon
            "100040265548",  # EX349DA -> EX349NL : Flat 2 Portland Villas, Hostle Park Road, Hostle Park Road, Ilfracombe, Devon
            "10000490826",  # EX349JA -> EX349JN : Conquest, Worth Road, Ilfracombe, Devon
            "10000484621",  # EX349EN -> EX349EL : Flat 2, Parliament Court Quayfield Road, Ilfracombe, Devon
            "10000484626",  # EX349EN -> EX349EL : Flat 8, Parliament Court Quayfield Road, Ilfracombe, Devon
            "10000484627",  # EX349EN -> EX349EL : Flat 9, Parliament Court Quayfield Road, Ilfracombe, Devon
            "10000484618",  # EX349EN -> EX349EL : Flat 10, Parliament Court Quayfield Road, Ilfracombe, Devon
            "10000484624",  # EX349EN -> EX349EL : Flat 5, Parliament Court Quayfield Road, Ilfracombe, Devon
            "10012112614",  # EX349HR -> EX349NR : Flat 1 Stafford House, 8 Hillsborough Terrace, Ilfracombe, Devon
            "100040265928",  # EX348PD -> EX348JL : Cedars, Marlborough Road, Ilfracombe, Devon
            "100041138737",  # EX348HA -> EX348LA : 2 Winsham Terrace, Ilfracombe, Devon
            "100041138738",  # EX348HA -> EX348LA : 3 Winsham Terrace, Ilfracombe, Devon
            "10012097008",  # EX348LL -> EX348LN : 2 Whitestone Cottage, Lincombe, Lee, Ilfracombe
            "10012098726",  # EX348LL -> EX348LN : 1 Whitestone Cottage, Lincombe, Lee, Ilfracombe
            "10012091795",  # EX314NB -> EX314ND : The Old Chapel House, Kentisbury Ford, Barnstaple
            "10090338353",  # EX314ND -> EX314NB : Beech Croft, Kentisbury Ford, Barnstaple
            "10090338354",  # EX314ND -> EX314NB : Bales Croft, Kentisbury Ford, Barnstaple
            "10090338355",  # EX314ND -> EX314NB : Rose Croft, Kentisbury Ford, Barnstaple
            "10000489210",  # EX314RF -> EX314RA : Highview Woolhanger Farm, Woolhanger, Parracombe, Barnstaple
            "10000487967",  # EX314DT -> EX314DU : Springfield Farm, Middle Marwood, Barnstaple, Devon
            "10090333861",  # EX363PT -> EX364RR : Little Moor Farm, Botreaux Mill, South Molton, Devon
            "10090337950",  # EX363NX -> EX364RR : Wild Boar Woodland, West Anstey, South Molton
            "100040243728",  # EX320PE -> EX327PE : 2 Caravan Birch Wood, Birch Road, Barnstaple, Devon
            "100040250867",  # EX329FQ -> EX329BQ : 47 A, Newport Road, Barnstaple, Devon.
            "10012099559",  # EX363QF -> EX364EH : Mill-Haven, Bish Mill, South Molton
            "10012098834",  # EX363EH -> EX363QU : Southlea Cottage, Southlea Service Station, Bish Mill, South Molton
            "10012098870",  # EX364DZ -> EX364NY : 1 Stonehouse, Bishops Nympton, South Molton, Devon
            "10012112080",  # EX364EH -> EX363EH : Clover Cottage, North Lee Farm, Hacche Lane, North Molton, South Molton, Devon
            "10012096422",  # EX363JT -> EX363JU : Lambscombe Farm, Lambscombe/upcott, North Molton, South Molton, Devon
            "10000488631",  # EX314RF -> EX314QJ : The Bungalow Sunnyside, Parracombe, Barnstaple, Devon
            "10000487950",  # EX314DR -> EX314DP : Sunny View, Bradiford, Barnstaple
            "10012114925",  # EX314JH -> EX314JJ : Caravan Brightlycott Cottage, Shirwell Road, Barnstaple, Devon
            "10012098311",  # EX320PA -> EX320PR : Mill Gardens, High Street, Swimbridge, Barnstaple, Devon
            "10000488923",  # EX312PA -> EX313PA : Alder Lodge, Eastacombe, Barnstaple
            "10012100160",  # EX313HU -> EX313HT : 2 Old Farm Court, Lake, Barnstaple, Devon
            "10012096203",  # EX313HU -> EX313HT : 4 Old Farm Court, Lake, Barnstaple, Devon
            "10012112161",  # EX394PF -> EX394PG : The Annexe, West Ashridge, Ashridge, Westleigh, Bideford, Devon
        ]:
            rec["accept_suggestion"] = True

        if uprn in [
            "100040248728",  # EX329DH -> EX329FG : Cranleigh, Kings Close, Landkey Road, Barnstaple
            "10012101664",  # EX329DH -> EX329FG : Clanfield, Kings Close, Landkey Road, Barnstaple
            "10012114702",  # EX327JJ -> EX314TY : View Farm, Bratton Fleming, Barnstaple, Devon
            "10012102258",  # EX328LL -> EX328LS : Flat 3 Lloyds Chambers, The Square, Barnstaple, Devon.
            "10000486532",  # EX340AS -> EX340AT : Flat 2 Bay View, Woodlands, Combe Martin, Devon
            "10000487730",  # EX313PH -> EX313PP : Hopesay Barn, East Woodlands, Newton Tracey, Barnstaple, Devon
            "10090337291",  # EX347HH -> EX347AT : Mobile Home 1 Smallacre Cottages, Mortehoe Station Road, Mortehoe, Woolacombe, Devon
            "10090337978",  # EX363EF -> EX314QN : Woodland Hideaway, Drewstone Farm, Bishops Nympton, South Molton, Devon
        ]:
            rec["accept_suggestion"] = False

        return rec
