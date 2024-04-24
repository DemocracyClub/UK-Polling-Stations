from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter
from django.contrib.gis.geos import Point


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "NWP"
    addresses_name = (
        "2024-05-02/2024-03-21T16:27:18.566958/Democracy_Club__02May2024.tsv"
    )
    stations_name = (
        "2024-05-02/2024-03-21T16:27:18.566958/Democracy_Club__02May2024.tsv"
    )
    elections = ["2024-05-02"]
    csv_encoding = "windows-1252"
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10093295441",  # TY TERNION, LODGE ROAD, CAERLEON, NEWPORT
            "10002155274",  # ORCHARD FARM, ST. BRIDES WENTLOOGE, NEWPORT
            "10002155651",  # BLUEBELL COTTAGE, ST. BRIDES WENTLOOGE, NEWPORT
            "100100646081",  # GREENFIELD HOUSE, TYLA LANE, OLD ST. MELLONS, CARDIFF
            "100100646082",  # GEM COTTAGE, TYLA LANE, OLD ST. MELLONS, CARDIFF
            "10002147773",  # WERN FARM, RHIWDERIN, NEWPORT
            "10014126660",  # MAISONETTE SECOND AND THIRD FLOOR 46 COMMERCIAL STREET, NEWPORT
            "10090277060",  # 6C TURNER STREET, NEWPORT
            "10090277061",  # 6B TURNER STREET, NEWPORT
            "10090277062",  # 6A TURNER STREET, NEWPORT
            "10010553788",  # 39 REMBRANDT WAY, NEWPORT
            "10002153590",  # RED ROBIN HOUSE, LLANDEVAUD, NEWPORT
            "10002153795",  # WOODLAND VIEW, PENHOW, CALDICOT
            "100100668792",  # YEW TREE COTTAGE, HENDREW LANE, LLANDEVAUD, NEWPORT
            "10002153732",  # SEYMOUR LODGE, PENHOW, CALDICOT
            "10002153780",  # HOLLY TREE COTTAGE, PENHOW, CALDICOT
            "10002153746",  # SEYMOUR COTTAGE, PENHOW, CALDICOT
            "10002153749",  # GROES WEN COTTAGE, PENHOW, CALDICOT
            "10014125572",  # MANAGERS ACCOMMODATION GROES WEN INN CHEPSTOW ROAD, NEWPORT
            "10093295775",  # THE OLD GARDEN, PONTYMASON LANE, ROGERSTONE, NEWPORT
            "100100654808",  # FIRST FLOOR FLAT 193 CARDIFF ROAD, NEWPORT
        ]:
            return None

        if record.post_code in [
            "NP10 8NT",  # split
            # suspect
            "NP10 8AT",
            "NP20 1LQ",
            "NP20 1HY",
            "NP20 7DY",
            "NP19 8AY",
            "NP20 3AF",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # Just Dance, Locke Street Community Centre, 8 Queens Hill, Newport, NP20 5HJ
        if record.polling_place_id == "13269":
            record = record._replace(polling_place_postcode="NP20 5HL")

        # The following are coordinates from the council:

        rec = super().station_record_to_dict(record)

        # All Saints Church, Brynglas Road, Newport, NP20 5QY
        if rec["internal_council_id"] == "13202":
            rec["location"] = Point(330874, 189624, srid=27700)
            return rec

        # St Michael`s Church, Church Road, Lower Machen, Newport, NP10 8GU
        if rec["internal_council_id"] == "13081":
            rec["location"] = Point(322799, 188082, srid=27700)
            return rec

        # St Patrick`s Church Hall, Cromwell Road, Newport, NP19 0HS
        if rec["internal_council_id"] == "13282":
            rec["location"] = Point(333129, 187604, srid=27700)
            return rec

        # Church Hall St Johns The Baptist Church, Oakfield Road, Newport, NP20 4LN
        if rec["internal_council_id"] == "12994":
            rec["location"] = Point(329952, 187756, srid=27700)
            return rec

        # Saint David Lewis Catholic Church, Brookside, Bettws, Newport, NP20 7DX
        if rec["internal_council_id"] == "13258":
            rec["location"] = Point(328991, 190909, srid=27700)
            return rec

        # St Teilo`s Church Hall, Aberthaw Avenue, Newport, NP19 9NS
        if rec["internal_council_id"] == "13003":
            rec["location"] = Point(334521, 187911, srid=27700)
            return rec

        # Beechwood House, Beechwood Park, Christchurch Road, Newport, NP19 8AJ
        if rec["internal_council_id"] == "13020":
            rec["location"] = Point(333261, 188646, srid=27700)
            return rec

        # Portable Unit, Kelly Road, Beechwood, Newport, NP19 7RF
        if rec["internal_council_id"] == "13018":
            rec["location"] = Point(332991, 189243, srid=27700)
            return rec

        # Portable Unit, Darwin Drive, Car Park next to Football Field, Malpas, NP20 6FS
        if rec["internal_council_id"] == "13142":
            rec["location"] = Point(330098, 190861, srid=27700)
            return rec

        # Michaelstone-Y-Fedw Village Hall, Michaelstone, Cardiff, CF3 6XS
        if rec["internal_council_id"] == "13146":
            rec["location"] = Point(324101, 184663, srid=27700)
            return rec

        # Portable Unit, outside Barracks, Allt-Yr-Yn View, Newport, NP20 5GG
        if rec["internal_council_id"] == "13268":
            rec["location"] = Point(330362, 189098, srid=27700)
            return rec

        # Gaer Baptist Church, Shakespeare Crescent, Newport, NP20 3LQ
        if rec["internal_council_id"] == "13066":
            rec["location"] = Point(329614, 186544, srid=27700)
            return rec

        # Bishton Village Hall, Bishton, Newport, NP18 2EA
        if rec["internal_council_id"] == "13098":
            rec["location"] = Point(338877, 187270, srid=27700)
            return rec

        # Portable Unit, Dos Road, Newport, NP20 5GJ
        if rec["internal_council_id"] == "13206":
            rec["location"] = Point(330836, 188980, srid=27700)
            return rec

        # Stow Park Community Centre, Brynhyfryd Road, Newport, NP20 4FX
        if rec["internal_council_id"] == "13054":
            rec["location"] = Point(330485, 187620, srid=27700)
            return rec

        # St Michael's Church Hall, Clarence Street, Pillgwenlly, Newport, NP20 2BZ
        if rec["internal_council_id"] == "13265":
            rec["location"] = Point(331819, 186829, srid=27700)
            return rec

        # Portable Unit, Ariel Reach, (opp Blaina Wharf car park), Pillgwenlly, Newport, NP20 2FR
        if rec["internal_council_id"] == "13267":
            rec["location"] = Point(332233, 186943, srid=27700)
            return rec

        # St Johns Hall, Chepstow Road, Newport, NP26 3AD
        if rec["internal_council_id"] == "13095":
            rec["location"] = Point(341528, 191133, srid=27700)
            return rec

        # Gateway Christian Centre, Castleton Baptist Church, 12 St Mellons Road, Marshfield, CF3 2TX
        if rec["internal_council_id"] == "13286":
            rec["location"] = Point(326010, 181990, srid=27700)
            return rec

        # St Julians Methodist Church, St Julians Avenue, Newport, NP19 7JT
        if rec["internal_council_id"] == "13221":
            rec["location"] = Point(332150, 189289, srid=27700)
            return rec

        # St David`s Church Hall, Bettws Hill, Bettws, Newport, NP20 7RS
        if rec["internal_council_id"] == "13034":
            rec["location"] = Point(328970, 190307, srid=27700)
            return rec

        # Redwick Village Hall, Church Row, Redwick, NP26 3DE
        if rec["internal_council_id"] == "13108":
            rec["location"] = Point(341296, 184159, srid=27700)
            return rec

        # Portable Unit, Old Barn Estate, Opposite 269 Buttermere Way, Newport, NP19 7BN
        if rec["internal_council_id"] == "13211":
            rec["location"] = Point(332491, 189712, srid=27700)
            return rec

        # Good Companions Club, Archibald Street, Newport, NP19 8EP
        if rec["internal_council_id"] == "13027":
            rec["location"] = Point(332511, 188171, srid=27700)
            return rec

        # Portable Unit, Church Crescent, Coedkernew, Newport, NP10 8TT
        if rec["internal_council_id"] == "13143":
            rec["location"] = Point(327338, 184400, srid=27700)
            return rec

        # Nash Community Hall, St Mary`s Road, Nash, Newport, NP18 2DD
        if rec["internal_council_id"] == "13128":
            rec["location"] = Point(334331, 183757, srid=27700)
            return rec

        # Cefn Wood Baptist Church, Ebenezer Drive, Rogerstone, Newport, NP10 9DP
        if rec["internal_council_id"] == "13323":
            rec["location"] = Point(327492, 187872, srid=27700)
            return rec

        # Pavillion Foyer, Belle Vue Park, NEWPORT, NP20 4FP
        if rec["internal_council_id"] == "13333":
            rec["location"] = Point(330608, 187170, srid=27700)
            return rec

        # St Brides Village Hall, Beach Road, St Brides, Newport, NP10 8SH
        if rec["internal_council_id"] == "13153":
            rec["location"] = Point(329770, 182345, srid=27700)
            return rec

        return super().station_record_to_dict(record)
