from django.contrib.gis.geos import Point

from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "COT"
    addresses_name = (
        "2023-05-04/2023-03-20T13:32:23.846470/Democracy_Club__04May2023.tsv"
    )
    stations_name = (
        "2023-05-04/2023-03-20T13:32:23.846470/Democracy_Club__04May2023.tsv"
    )
    elections = ["2023-05-04"]
    csv_encoding = "windows-1252"
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10022838989",  # CORNER COTTAGE, TRULL, TETBURY
            "10023475981",  # SELWORTHY, MORETON ROAD, STOW ON THE WOLD, CHELTENHAM
            "10013878640",  # BARTON MEADOW LODGE, GUITING POWER, CHELTENHAM
            "10093270137",  # WOODLAND BARN FARM, WHITEWAY, CIRENCESTER
            "200002916722",  # THE FIRS, NORTHWICK PARK, BLOCKLEY, MORETON-IN-MARSH
            "10095336680",  # MANAGERS ACCOMODATION THE GALLERIES DITCHFORD ROAD, TODENHAM
            "10095336266",  # GALLOP BOTTOM, GRANGE HILL, NAUNTON, CHELTENHAM
            "10013392804",  # WOODLANDS FARM, WHITTINGTON, CHELTENHAM
            "10013886740",  # THE STABLE FLAT HARTLEY FARM HARTLEY LANE, LECKHAMPTON HILL, COBERLEY
            "10013886813",  # HARTLEY FARM, HARTLEY LANE, LECKHAMPTON HILL, CHELTENHAM
            "100120433798",  # STARVEALL COTTAGE, STROUD ROAD, BIRDLIP, GLOUCESTER
            "100121238347",  # HEATH HOUSE, GLOUCESTER ROAD, CIRENCESTER
            "10095337476",  # 1 ROOKERY FIELD, WOODMANCOTE, CIRENCESTER
            "10095337477",  # 2 ROOKERY FIELD, WOODMANCOTE, CIRENCESTER
            "10095337478",  # 3 ROOKERY FIELD, WOODMANCOTE, CIRENCESTER
            "10013392569",  # LYDE COTTAGE, UPPER COBERLEY, CHELTENHAM
        ]:
            return None

        if record.addressline6 in [
            "GL7 5RA",
            "GL7 3PR",
            "GL54 5US",
            "GL54 1LT",
            "GL55 6LW",
            "GL56 9NF",
            "GL54 3ER",
            "GL54 3LX",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # Leighterton Primary School, Leighterton, GL8 8UH
        # correction from council
        if record.polling_place_id == "21286":
            record = record._replace(
                polling_place_easting="382121",
                polling_place_northing="191316",
            )

        # Bingham Hall, Bingham Hall, King Street, Cirencester, GL7 1JT
        # correction from council
        if record.polling_place_id == "23487":
            record = record._replace(
                polling_place_easting="402792",
                polling_place_northing="201385",
            )

        # Tetbury Goods Shed Arts Centre, GL8 8EY
        # correction from council
        if record.polling_place_id == "21417":
            record = record._replace(
                polling_place_easting="389331",
                polling_place_northing="193235",
            )

        rec = super().station_record_to_dict(record)

        # St Mary`s Church, Meysey Hampton, GL7 5JS
        if rec["internal_council_id"] == "23508":
            rec["location"] = Point(-1.831982, 51.699177, srid=4326)

        return rec
