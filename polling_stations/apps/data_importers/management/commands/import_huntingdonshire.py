from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "HUN"
    addresses_name = "2021-03-22T10:17:22.245616/Democracy_Club__06May2021 Friday.CSV"
    stations_name = "2021-03-22T10:17:22.245616/Democracy_Club__06May2021 Friday.CSV"
    elections = ["2021-05-06"]
    csv_delimiter = ","

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10094922851",  # CAMELLIA COTTAGE, LITTLE END ROAD, EATON SOCON, ST. NEOTS
            "10094922852",  # 156B GREAT NORTH ROAD, EATON SOCON
            "10093629694",  # 156A GREAT NORTH ROAD, EATON SOCON
            "10093628232",  # 78 HARTFORD ROAD, HUNTINGDON
            "10093626016",  # 1A ELM DRIVE, ST. IVES
            "10090393780",  # 4A ST. AUDREY LANE, ST. IVES
            "10090393781",  # 4C ST. AUDREY LANE, ST. IVES
            "10090393783",  # 4 ST. AUDREY LANE, ST. IVES
            "10090393782",  # 4B ST. AUDREY LANE, ST. IVES
            "100091201367",  # THE HAWTHORNS, WOOD LANE, RAMSEY, HUNTINGDON
            "10091593436",  # 26D ALEXANDRA HOUSE HINCHINGBROOKE HOSPITAL HINCHINGBROOKE PARK ROAD, HUNTINGDON
            "10012049676",  # NEW FARM, EARITH ROAD, COLNE, HUNTINGDON
        ]:
            return None

        if record.addressline6 in [
            "PE26 1HA",
            "PE27 5BZ",
            "PE19 1HW",
            "PE26 2UB",
            "PE28 2AS",
            "PE29 2PL",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):

        # Removing unwanted text from polling station name.
        if "NEW POLLING STATION" in record.polling_place_name:
            record = record._replace(
                polling_place_name=record.polling_place_name.replace(
                    "NEW POLLING STATION:", ""
                )
            )

        # Berkley Street Methodist Church, Berkley Street, Eynesbury, St. Neots, PE19 2HD
        if record.polling_place_id == "7819":
            record = record._replace(polling_place_postcode="PE19 2NB")

        if record.polling_place_id in [
            "7643"  # Ellington Village Hall, Ellington
            "7620"  # Colne Community Hall, East Street, Colne
        ]:
            record = record._replace(polling_place_postcode="")

        return super().station_record_to_dict(record)
