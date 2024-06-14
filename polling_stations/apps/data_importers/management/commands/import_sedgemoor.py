from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "SEG"
    addresses_name = "2024-07-04/2024-06-21T16:09:14.537768/SEG_combined.csv"
    stations_name = "2024-07-04/2024-06-21T16:09:14.537768/SEG_combined.csv"
    elections = ["2024-07-04"]
    not_in_sedgemoor_stations = [
        "501-chewton-mendip-village-hall",
        "502-croscombe-village-hall",
        "503-binegar-memorial-hall",
        "504-godney-village-hall",
        "505-litton-village-hall",
        "506-meare-church-rooms",
        "507-north-wootton-village-hall",
        "508-pilton-village-hall",
        "509-priddy-village-hall",
        "510-draycott-memorial-hall",
        "511-somerset-council",
        "512-somerset-council",
        "513-somerset-council",
        "514-somerset-council",
        "515-wells-golf-club",
        "516-wookey-hole-caves",
        "517-easton-village-hall",
        "518-dinder-village-hall",
        "519-coxley-memorial-hall",
        "520-ston-easton-village-hall",
        "521-clapton-village-hall",
        "522-walton-village-hall",
        "523-wells-elim-connect-centre",
        "524-wells-the-portway-annexe",
        "525-wells-the-portway-annexe",
        "526-wells-st-thomas-church-hall",
        "527-wells-st-thomas-church-hall",
        "528-westbury-sub-mendip-village-hall",
        "529-wookey-church-hall",
    ]

    def address_record_to_dict(self, record):
        station_hash = self.get_station_hash(record)
        if station_hash in self.not_in_sedgemoor_stations:
            return None
        uprn = record.uprn.strip()

        if uprn in [
            "10090855892",  # PUT HOUSE, FIDDINGTON, BRIDGWATER, TA51JW
            "100040899479",  # 135A TAUNTON ROAD, BRIDGWATER, TA6 6BD
            "10009322907",  # CHESTNUT HOUSE, EASTERTOWN, LYMPSHAM, WESTON-SUPER-MARE
            "10009320475",  # RIVERSIDE FARM, BIDDISHAM LANE, BIDDISHAM, AXBRIDGE
            "200000444031",  # POOLBRIDGE FARM HOUSE POOLBRIDGE ROAD, BLACKFORD, WEDMORE
            "200000449171",  # HILLFURLONG, CHILTON POLDEN HILL, BRIDGWATER
            "10090856797",  # OWERY BARN OWERY FARM OWERY FARM LANE, MIDDLEZOY, BRIDGWATER
            "10009328298",  # OWERY FARM, MIDDLEZOY, BRIDGWATER
            "200001842896",  # OLD COTTAGE, PIGHTLEY, SPAXTON, BRIDGWATER
            "200000439799",  # THE SLADES, BROOMYLAND HILL, SPAXTON, BRIDGWATER
            "200000451064",  # WRENMORE ELMS, FIDDINGTON, BRIDGWATER
            "10009318823",  # CHESTNUT HOUSE, DOWNEND ROAD, PURITON, BRIDGWATER
            "10009327419",  # PEDWA BARNS, HUNTSPILL ROAD, HIGHBRIDGE
            "100040907181",  # PRIORY COURT CARE HOME, 19 OXFORD STREET, BURNHAM-ON-SEA
            "10009323643",  # FLAT 1, 20 COLLEGE STREET, BURNHAM-ON-SEA
            "10090856573",  # 6 THE GABLES, ALLANDALE ROAD, BURNHAM-ON-SEA
            "10023415613",  # 15A ALLANDALE ROAD, BURNHAM-ON-SEA
            "200000448816",  # RIVERSIDE FARM, LOWER WEARE, AXBRIDGE
            "200000450711",  # GOLD CORNER BUNGALOW, EAST HUNTSPILL, HIGHBRIDGE
            "100040887755",  # CROSSING COTTAGE, GOOSE LANE, CHILTON POLDEN, BRIDGWATER
            "100041114944",  # HOMESTILL BUNGALOW, BLAKEWAY, WEDMORE
            "10009328207",  # LITTLE ORCHARD FARM, WASHBROOK, WEDMORE
            "10009328197",  # NEW TYNING, STONE ALLERTON, AXBRIDGE
            "200000446874",  # LAMBRIDGE HOUSE, SPAXTON, BRIDGWATER
            "10009323237",  # HALLICKS FARM, CHILTON TRINITY, BRIDGWATER
            "200000445815",  # NORTHOVER, FIDDINGTON, BRIDGWATER
        ]:
            return None

        if record.housepostcode in [
            # splits
            "BS27 3EP",
            "TA6 4HB",
            "TA6 6RZ",
            "TA5 2PF",
            "TA6 6QH",
            "TA6 5NL",
            "TA6 6LJ",
            "TA6 7BS",
            "TA6 6LR",
            "TA6 6GD",
            # suspect
            "BS24 0HD",  # BREAN ROAD, LYMPSHAM, WESTON-SUPER-MARE
            "TA7 9AG",  # FORD LODGE, STAWELL, BRIDGWATER
            "TA9 4HP",  # SOUTH VIEW, BRIDGWATER ROAD, EAST BRENT, HIGHBRIDGE
            "TA9 4HL",  # BRISTOL ROAD, BRENT KNOLL, HIGHBRIDGE
            "BS24 0HD",  # BREAN ROAD, LYMPSHAM, WESTON-SUPER-MARE
            "TA8 2RW",  # THE PILLARS RED ROAD, BERROW, BURNHAM-ON-SEA
            "TA6 4DF",  # CASTLEFIELDS COTTAGES, CASTLEFIELDS, BRIDGWATER
            "TA94RB",  # WATCHFIELD, HIGHBRIDGE
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        station_hash = self.get_station_hash(record)
        if station_hash in self.not_in_sedgemoor_stations:
            return None

        return super().station_record_to_dict(record)
