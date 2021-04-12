from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "NBL"
    addresses_name = "2021-03-25T12:14:50.419215/Democracy_Club__06May2021.tsv"
    stations_name = "2021-03-25T12:14:50.419215/Democracy_Club__06May2021.tsv"
    elections = ["2021-05-06"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        if record.addressline6 in [
            "NE61 3FF",
            "NE61 6JD",
            "NE63 0FD",
            "NE48 1HR",
            "NE47 7AQ",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        if record.polling_place_id in [
            "3488",  # Thropton War Memorial Hall, Thropton, Morpeth, Northumberland NE65 7LR
            "3519",  # Hadston Druridge Bay Community Centre, Hadston Precinct, Hadston, Morpeth, Northumberland NE65 9SR
            "3541",  # Ingram Village Hall, Ingram, Powburn, Alnwick, Northumberland NE66 4LU
            "3578",  # North Sunderland & Seahouses Sports & Community Centre, Seahouses, Northumberland NE68 7TP
            "3502",  # Felton Village Hall, Felton, Morpeth, Northumberland NE65 9PT
            "3650",  # Alnwick Lindisfarne Sports Centre, Victoria Crescent, Alnwick, Northumberland NE66 1AX
            "3784",  # Seaton Delaval United Reformed/Methodist Church Hall, Elsdon Avenue, Seaton Delaval, Northumberland NE25 0BW
            "3620",  # Netherwitton Village Hall, Netherwitton, Morpeth, Northumberland NE61 4NW
            "3635",  # Craster Memorial Hall, Craster, Alnwick, Northumberland NE66 3TP
            "3719",  # Holy Island Crossman Village Hall, Holy Island, Berwick-Upon-Tweed TD15 2ST
            "3764",  # Cramlington Nelson Village Welfare Community Centre, 55 Nelson Avenue, Nelson Village, Cramlington, Northumberland NE23 1HG
            "3799",  # Blyth Briardale House Youth and Community Project, Briardale Road, Cowpen Estate, Blyth, Northumberland NE24 5AN
            "3660",  # Powburn Breamish Hall, Powburn, Alnwick, Northumberland NE66 4HL
            "3664",  # Boulmer Memorial Hall, Boulmer, Alnwick, Northumberland NE66 0RA
            "3592",  # Berwick St Cuthberts Parish Centre, Walkergate, Berwick Upon Tweed TD15 1DS
            "3713",  # Etal Village Hall, Etal, Berwick Upon Tweed TD12 4TN
            "3816",  # Blyth Neptune Hq, Scout Building, Fulmar Drive, South Beach, Blyth NE24 3RJ
            "3566",  # Bamburgh Pavilion, Bamburgh, Northumberland NE69 7BP
            "3850",  # Horsley Village & Wi Hall, Horsley, Newcastle Upon Tyne NE15 0NS
            "3936",  # Hexham West End Methodist Church Hall, Shaftoe Leazes, Hexham, Northumberland NE46 3DF
            "3985",  # Ponteland United Reformed Church, Broadway, Ponteland, Newcastle Upon Tyne NE20 9PP
            "3991",  # Stamfordham Village Hall, Stamfordham, Newcastle Upon Tyne NE18 0NA
            "4015",  # Allenheads Heritage Centre, Allenheads, Northumberland NE47 9HN
            "3898",  # Bellingham Town Hall, Front Street, Bellingham, Hexham, Northumberland NE48 2AA
            "3956",  # Wall Village Hall, Wall, Hexham, Northumberland NE46 4DX
            "3879",  # Featherstone Village Hall, Featherstone, Northumberland NE49 0JG
            "4028",  # Slaley Commemoration Hall, Main Street, Slaley, Hexham, Northumberland NE47 0AA
            "4061",  # Byrness Village Hall, Byrness, Northumberland NE19 1TT
            "4019",  # Catton Village Hall, Catton, Northumberland NE47 9QH
            "4136",  # Cambois Camera Club, Ridley Terrace, Cambois, Northumberland NE24 1QS
            "4153",  # Bedlington Doctor Pit Pavilion, Doctor Pit Park, Park Road, Bedlington, Northumberland NE22 5DA
            "4126",  # Newbiggin Elizabethan Hall, Hepple Road, Newbiggin By the Sea, Northumberland NE64 6SR
            "4080",  # Hepscott Parish Hall, Hepscott, Morpeth, Northumberland NE61 6LT
            "4082",  # Mitford Community Centre, Fontside, Mitford, Morpeth, Northumberland NE61 3PS
        ]:
            record = record._replace(polling_place_postcode="")

        # Guide Post Scouts Hut, Olympia Avenue, Guide Post, Choppington, Northumberland, NE62 5DF
        if record.polling_place_id == "4066":
            record = record._replace(polling_place_uprn="")

        return super().station_record_to_dict(record)
