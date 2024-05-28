from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "NBL"
    addresses_name = (
        "2024-07-04/2024-05-28T12:57:30.578981/Democracy_Club__04July2024.tsv"
    )
    stations_name = (
        "2024-07-04/2024-05-28T12:57:30.578981/Democracy_Club__04July2024.tsv"
    )
    elections = ["2024-07-04"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10096301305",  # 4 MARINA WEST, AMBLE, MORPETH
            "10096301304",  # 5 MARINA WEST, AMBLE, MORPETH
            "200002823696",  # ST. AIDANS PRIMARY SCHOOL HOUSE, MOORHOUSE LANE, ASHINGTON
            "10094015954",  # 7 HARRISON CRESCENT, ESSENDENE RISE, NORTH SEATON, ASHINGTON
            "10012421608",  # LANE END FARM, NEWBIGGIN ROAD, NORTH SEATON, ASHINGTON
            "10032938120",  # THE BIRCHES, RED ROW DRIVE, BEDLINGTON
            "10000843358",  # EBENEEZER, CARRSHIELD, HEXHAM
            "10000844527",  # EAST HOT BANK FARM, BARDON MILL, HEXHAM
            "200000923540",  # GRINDON HILL BUNGALOW, HAYDON BRIDGE, HEXHAM
            "10001018037",  # COALSFIELD HOUSE, ELSDON, NEWCASTLE UPON TYNE
            "200000919007",  # FARGLOW FARM, GREENHEAD, BRAMPTON
        ]:
            return None

        if record.addressline6 in [
            # splits
            "NE61 6JD",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # Council requested to drop all the changes and use data provided by them
        # Ignore all the warnings, below corrections commented out for future references

        # # 'The Lindisfarne Centre, Lindisfarne Road, Alnwick, NE66 1AX' (id: 8235)
        # # postcode provided by the council, ignore the warning
        #
        # # 'Bamburgh Pavilion, Bamburgh, NE69 7BP' (id: 8144)
        # # postcode provided by the council, ignore the warning
        # if record.polling_place_id == "8144":
        #     record = record._replace(polling_place_postcode="NE69 7DB")
        #
        # # 'St Cuthberts Parish Centre, Walkergate, Berwick upon Tweed, TD15 1DS' (id: 8176)
        # # postcode provided by the council, ignore the warning
        # if record.polling_place_id == "8176":
        #     record = record._replace(polling_place_postcode="TD15 2SB")
        #
        # # 'Netherwitton Village Hall, Netherwitton, Morpeth, NE61 4NW' (id: 8204)
        # # postcode provided by the council, ignore the warning
        #
        # # 'Felton Village Hall, Felton, Morpeth, NE65 9PT' (id: 8076)
        # if record.polling_place_id == "8076":
        #     record = record._replace(polling_place_postcode="NE65 9NH")
        #
        # # 'Ellingham Village Hall, Ellingham, NE67 5HA' (id: 8236)
        # # postcode provided by the council, ignore the warning
        #
        # # 'Boulmer Memorial Hall, Boulmer, Alnwick, NE66 0RA' (id: 8248)
        # if record.polling_place_id == "8248":
        #     record = record._replace(polling_place_postcode="NE66 3BP")
        #
        # # 'Etal Village Hall, Etal, Berwick upon Tweed, TD12 4TN' (id: 8306)
        # if record.polling_place_id == "8306":
        #     record = record._replace(polling_place_postcode="TD12 4TL")
        #
        # # 'Holy Island Crossman Village Hall, Holy Island, Berwick upon Tweed, TD15 2ST' (id: 8314)
        # # postcode provided by the council, ignore the warning
        # if record.polling_place_id == "8314":
        #     record = record._replace(polling_place_postcode="TD15 2RX")
        #
        # # 'Ingram Village Hall, Ingram, Powburn, Alnwick, NE66 4LU' (id: 8117)
        # # postcode provided by the council, ignore the warning
        #
        # # 'Nelson Village Welfare Community Centre, 55 Nelson Avenue, Nelson Village, Cramlington, NE23 1HG' (id: 8362)
        # # postcode provided by the council, ignore the warning
        #
        # # 'Seaton Delaval United Reformed/Methodist Church Hall, Elsdon Avenue, Seaton Delaval, NE25 0BW' (id: 8386)
        # # postcode provided by the council, ignore the warning
        #
        # # 'Blyth Briardale House Youth and Community Project, Briardale Road, Cowpen Estate, Blyth, NE24 5AN' (id: 8399)
        # # postcode provided by the council, ignore the warning
        #
        # # 'Blyth Saint Benedicts Church, Devonworth Place, Blyth, NE24 5AD' (id: 8397)
        # # postcode provided by the council, ignore the warning
        # if record.polling_place_id == "8397":
        #     record = record._replace(polling_place_postcode="NE24 5AU")
        #
        # # 'Bellingham Town Hall, Front Street, Bellingham, Hexham, NE48 2AA' (id: 8509)
        # # postcode provided by the council, ignore the warning
        # if record.polling_place_id == "8509":
        #     record = record._replace(polling_place_postcode="NE48 2AH")
        #
        # # 'Byrness Village Hall, Byrness, NE19 1TT' (id: 8699)
        # # postcode provided by the council, ignore the warning
        #
        # # 'Horsley Village Hall Trust, Horsley, NE15 0NS' (id: 8457)
        # if record.polling_place_id == "8457":
        #     record = record._replace(polling_place_postcode="NE15 0NT")
        #
        # # 'Featherstone Village Hall, Featherstone, NE49 0JG' (id: 8488)
        # if record.polling_place_id == "8488":
        #     record = record._replace(polling_place_postcode="NE49 0JE")
        #
        # # 'Hexham West End Methodist Church Hall, Shaftoe Leazes, Hexham, NE46 3DF' (id: 8547)
        # # postcode provided by the council, ignore the warning
        #
        # # 'Wall Village Hall, Wall, Hexham, NE46 4DX' (id: 8570)
        # if record.polling_place_id == "8570":
        #     record = record._replace(polling_place_postcode="NE46 4DU")
        #
        # # 'Matfen Village Hall, Matfen, NE20 0RP' (id: 8609)
        # # postcode provided by the council, ignore the warning
        #
        # # 'Stamfordham Village Hall, Stamfordham, NE18 0NA' (id: 8613)
        # # postcode provided by the council, ignore the warning
        #
        # # 'Catton Village Hall, Catton, NE47 9QH' (id: 8648)
        # # postcode provided by the council, ignore the warning
        #
        # # 'Blanchland Village Hall, Derwent View, Blanchland, Consett, DH8 9UA' (id: 8655)
        # # postcode provided by the council, ignore the warning
        #
        # # 'Slaley Commemoration Hall, Main Street, Slaley, Hexham, NE47 0AA' (id: 8659)
        # if record.polling_place_id == "8659":
        #     record = record._replace(polling_place_postcode="NE47 0BQ")
        #
        # # 'Scouts Hut, Olympia Avenue, Guide Post, Choppington, NE62 5DF' (id: 8705)
        # # postcode provided by the council, ignore the warning
        #
        # # 'Hepscott Parish Hall, Hepscott, Morpeth, NE61 6LT' (id: 8722)
        # if record.polling_place_id == "8722":
        #     record = record._replace(polling_place_postcode="NE61 6LN")
        #
        # # 'Mitford Community Centre, Fontside, Mitford, Morpeth, NE61 3PS' (id: 8724)
        # # postcode provided by the council, ignore the warning
        #
        # # 'Cambois Camera Club, Ridley Terrace, Cambois, NE24 1QS' (id: 8783)
        # # postcode provided by the council, ignore the warning

        return super().station_record_to_dict(record)
