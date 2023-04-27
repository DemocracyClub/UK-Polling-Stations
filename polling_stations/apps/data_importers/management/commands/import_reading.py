from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "RDG"
    addresses_name = (
        "2023-05-04/2023-03-27T11:54:03.935496/Democracy_Club__04May2023.CSV"
    )
    stations_name = (
        "2023-05-04/2023-03-27T11:54:03.935496/Democracy_Club__04May2023.CSV"
    )
    elections = ["2023-05-04"]

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "310084857",  # FLAT 2, 69 NORTHUMBERLAND AVENUE, READING
            "310084859",  # FLAT 4, 69 NORTHUMBERLAND AVENUE, READING
            "310084858",  # FLAT 3, 69 NORTHUMBERLAND AVENUE, READING
            "310064645",  # 1 STAR ROAD, CAVERSHAM, READING
            "310047121",  # BEECH HOUSE HOTEL, 60 BATH ROAD, READING
            "310057403",  # 66 ALEXANDRA ROAD, READING
            "310008722",  # 64 ALEXANDRA ROAD, READING
        ]:
            return None

        if record.addressline6 in [
            # splits
            "RG30 3NB",
            "RG30 4RX",
            "RG4 8ES",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # Reading Central Library, Abbey Square, Reading, RG1 3BG
        if record.polling_place_id == "4313":
            record = record._replace(polling_place_postcode="RG1 3BQ")

        # Park Lounge, Windsor Hall, University of Reading, Upper Redlands Road, Reading, RG1 5JL
        if record.polling_place_id == "4455":
            record = record._replace(polling_place_postcode="RG6 6HW")

        # Museum of English Rural Life,6  Redlands Road, RG1 5EX
        # correction for the council
        # >> WARNING: Geocoding with UPRN. Station record postcode does not match addressbase postcode.
        # >> Checked, postcode from the CSV is correct, no action required
        if record.polling_place_id == "4442":
            record = record._replace(polling_place_uprn="310067634")

        # Sir Herman Gollancz Hall, Clifton Street, Reading,RG1 7YE
        # correction for the council
        if record.polling_place_id == "4306":
            record = record._replace(polling_place_uprn="310065169")

        # Reading Central Library, Abbey Square, Reading, RG1 3BG
        # correction for the council
        if record.polling_place_id == "4313":
            record = record._replace(polling_place_uprn="310048086")

        # Emmanuel Methodist Church, 448 Oxford Road, Reading, RG30 1EE
        # correction for the council
        if record.polling_place_id == "4326":
            record = record._replace(polling_place_uprn="310068291")

        # 420 Battle Library, Oxford Road, Reading, Berkshire, RG30 1EE,
        # correction for the council
        if record.polling_place_id == "4333":
            record = record._replace(polling_place_uprn="310058680")

        # New Bridge Nursery School, Montague Street,Caversham, RG4 5AU,310027239
        # correction for the council
        if record.polling_place_id == "4340":
            record = record._replace(polling_place_uprn="")

        # The Weller Centre, 110 Amersham Road, Caversham, Reading, RG4 5NA,
        # correction for the council
        if record.polling_place_id == "4344":
            record = record._replace(polling_place_uprn="310068855")

        # Caversham Library, Church Street, Caversham, RG4 8AU,
        # correction for the council
        if record.polling_place_id == "4337":
            record = record._replace(polling_place_uprn="310052373")

        # Caversham Heights Methodist Church, 74 Highmoor Road, Caversham, RG4 7BG,
        # correction for the council
        if record.polling_place_id == "4348":
            record = record._replace(polling_place_uprn="310007911")

        # Surley Row, Caversham, Reading, RG4 8LR,
        # correction for the council
        if record.polling_place_id == "4359":
            record = record._replace(polling_place_uprn="310027569")

        # St Andrew`s Church Hall, Albert Road,Caversham, RG4 7PW,
        # correction for the council
        if record.polling_place_id == "4355":
            record = record._replace(polling_place_uprn="310043512")

        # Mapledurham Pavilion, Upper Woodcote Road, Caversham,
        # correction for the council
        if record.polling_place_id == "4351":
            record = record._replace(polling_place_uprn="310069801")

        # St Barnabas Church Hall, Elm Road, Reading, RG6 5TS,
        # correction for the council
        if record.polling_place_id == "4367":
            record = record._replace(polling_place_uprn="310058852")

        # South Reading Community Hub, 252 Northumberland Avenue, RG2 7QA,
        # correction for the council
        if record.polling_place_id == "4371":
            record = record._replace(polling_place_uprn="310027887")

        # WHITLEY PARK PRIMARY & NURSERY SCHOOL, Brixham Road,READING, RG2 7RB,
        # correction for the council
        if record.polling_place_id == "4375":
            record = record._replace(polling_place_uprn="310076550")

        # Coley Primary School, Wolesley Street, RG1 6AZ,
        # correction for the council
        if record.polling_place_id == "4379":
            record = record._replace(polling_place_uprn="310009744")

        # All Saints Hall, Downshire Square, RG1 6NJ,
        # correction for the council
        if record.polling_place_id == "4383":
            record = record._replace(polling_place_uprn="310042621")

        # Coley Park Community Centre,140  Wensley Road, RG1 6DW,
        # correction for the council
        if record.polling_place_id == "4386":
            record = record._replace(polling_place_uprn="310023330")

        # Emmer Green Youth &  Com Centre, St Barnabas Road, Emmer Green, RG4 8RA,
        # correction for the council
        if record.polling_place_id == "4389":
            record = record._replace(polling_place_uprn="310052389")

        # Milestone Centre, Milestone Way, Caversham, RG4 6PF,
        # correction for the council
        if record.polling_place_id == "4392":
            record = record._replace(polling_place_uprn="310027343")

        # Mickland`s County Primary School, Micklands Road, Caversham, RG4 6LU,
        # correction for the council
        if record.polling_place_id == "4395":
            record = record._replace(polling_place_uprn="310038664")

        # Katesgrove Primary School, Dorothy Street, RG1 2NL,
        # correction for the council
        if record.polling_place_id == "4399":
            record = record._replace(polling_place_uprn="310031942")

        # Christchurch Centre, Milman Road, RG2 0AY,
        # correction for the council
        if record.polling_place_id == "4403":
            record = record._replace(polling_place_uprn="310069991")

        # The Palmer Academy, 70 Northumberland Avenue, RG2 7PP,
        # correction for the council
        if record.polling_place_id == "4407":
            record = record._replace(polling_place_uprn="310079044")

        # Coley Primary School, Wolesley Street, RG1 6AZ,
        # correction for the council
        if record.polling_place_id == "4379":
            record = record._replace(polling_place_uprn="310009744")

        # St Mary Magdalene Church Hall, Rodway Road, Tilehurst, RG31 6DR,
        # correction for the council
        if record.polling_place_id == "4410":
            record = record._replace(polling_place_uprn="310069568")

        # United Reformed Church Hall, Polsted Road, Tilehurst, RG31 6HN,
        # correction for the council
        if record.polling_place_id == "4413":
            record = record._replace(polling_place_uprn="310018955")

        # Meadow Park Academy, Norcot Road, Tilehurst, RG30 6BS,310078492
        # correction for the council
        if record.polling_place_id == "":
            record = record._replace(polling_place_uprn="")

        # Lyndhurst Road,Tilehurst, RG30 6UB,
        # correction for the council
        if record.polling_place_id == "4419":
            record = record._replace(polling_place_uprn="310034328")

        # St George`s Church, St Georges Road, RG30 2RJ,
        # correction for the council
        if record.polling_place_id == "4421":
            record = record._replace(polling_place_uprn="310035046")

        # St Michael`s Primary School, Dee Road, Tilehurst, RG30 4AS,
        # correction for the council
        if record.polling_place_id == "4425":
            record = record._replace(polling_place_uprn="310039942")

        #
        # correction for the council
        if record.polling_place_id == "":
            record = record._replace(polling_place_uprn="")

        # New Town Primary School, School Terrace, RG1 3LS,
        # correction for the council
        if record.polling_place_id == "4432":
            record = record._replace(polling_place_uprn="310025872")

        # Alfred Sutton Primary School, Wokingham Road, RG6 0PF,
        # correction for the council
        if record.polling_place_id == "4435":
            record = record._replace(polling_place_uprn="310024625")

        # Wesley Church Hall, Queens Road, RG1 4BW,
        # correction for the council
        if record.polling_place_id == "4438":
            record = record._replace(polling_place_uprn="310044611")

        # St. Luke`s Church Hall, Erleigh Road, RG1 5LU,
        # correction for the council
        if record.polling_place_id == "4448":
            record = record._replace(polling_place_uprn="310051510")

        # Hexham Community Centre, 1A Bamburgh Close, RG2 7UD,
        # correction for the council
        if record.polling_place_id == "4451":
            record = record._replace(polling_place_uprn="310023446")

        # Park Lounge, Windsor Hall, Windsor Hall, UoR, Park Lounge, Upper Redlands Road,, RG1 5JL,
        # correction for the council
        if record.polling_place_id == "4455":
            record = record._replace(polling_place_uprn="310041328")

        # Southcote C P School, Silchester Road, RG30 3EJ,
        # correction for the council
        if record.polling_place_id == "4470":
            record = record._replace(polling_place_uprn="310047136")

        # Manor C P School, 110 Ashampstead Road, Southcote, RG30 3LG
        # correction for the council
        if record.polling_place_id == "4462":
            record = record._replace(polling_place_uprn="310016595")
            record = record._replace(polling_place_postcode="RG30 3LJ")

        # Southcote Community Hub, Southcote Lane,Southcote, RG30 3BA,
        # correction for the council
        if record.polling_place_id == "4470":
            record = record._replace(polling_place_uprn="310069572")

        # Reading YMCA, Milward Centre, 34 Parkside Road,, RG30 2DD,
        # correction for the council
        if record.polling_place_id == "4471":
            record = record._replace(polling_place_uprn="310078395")

        # Community Centre,York Road, RG1 8DU,
        # correction for the council
        if record.polling_place_id == "4472":
            record = record._replace(polling_place_uprn="310069506")

        # St John`s and St Stephen Parish Centre, Orts Road, RG1 3JN,
        # correction for the council
        if record.polling_place_id == "4476":
            record = record._replace(polling_place_uprn="310076517")

        # Thameside Primary School,  Harley Road,Caversham, RG4 8DB,
        # correction for the council
        if record.polling_place_id == "4480":
            record = record._replace(polling_place_uprn="310001048")

        # Moorlands CP School, Church End Lane, RG30 4UN,
        # correction for the council
        if record.polling_place_id == "4483":
            record = record._replace(polling_place_uprn="310035564")

        # The Royal British Legion, Downing Road, Tilehurst, RG31 5BB,
        # correction for the council
        if record.polling_place_id == "4486":
            record = record._replace(polling_place_uprn="310050313")

        # Tilehurst Village Hall, Victoria Road,Tilehurst, RG31 5AB,
        # correction for the council
        if record.polling_place_id == "4490":
            record = record._replace(polling_place_uprn="310003050")

        # Christ the King Church Hall, 408 Northumberland Avenue, RG2 8NR,
        # correction for the council
        if record.polling_place_id == "4498":
            record = record._replace(polling_place_uprn="310034114")

        # Whitley Wood Community Centre, Swallowfield Drive, RG2 8UT,
        # correction for the council
        if record.polling_place_id == "4501":
            record = record._replace(polling_place_uprn="310065921")

        # 100 Longwater Avenue, Green Park, Whitley PC, 100 Longwater Avenue, Reading, RG2 6GP,
        # correction for the council
        if record.polling_place_id == "4505":
            record = record._replace(polling_place_uprn="310063437")

        # Kennet Island Community Centre, Havergate Way, Reading, RG2 OGU,
        # correction for the council
        if record.polling_place_id == "4494":
            record = record._replace(polling_place_uprn="310070321")
            record = record._replace(polling_place_postcode="RG2 0GU")

        # South Reading Leisure Centre, Northumberland Avenue, RG2 8DF,
        # correction for the council
        if record.polling_place_id == "4506":
            record = record._replace(polling_place_uprn="310038210")

        return super().station_record_to_dict(record)
