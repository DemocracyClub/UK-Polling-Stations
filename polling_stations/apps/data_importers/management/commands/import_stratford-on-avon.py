from django.contrib.gis.geos import Point

from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "STR"
    addresses_name = (
        "2023-05-04/2023-03-07T09:03:03.694104/Democracy_Club__04May2023.tsv"
    )
    stations_name = (
        "2023-05-04/2023-03-07T09:03:03.694104/Democracy_Club__04May2023.tsv"
    )
    elections = ["2023-05-04"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10024063650",  # THE STUDIO, CUTLERS FARM, EDSTONE, WOOTTON WAWEN, HENLEY-IN-ARDEN
            "100071249390",  # KINGSTON HOLT FARM, BANBURY ROAD, LIGHTHORNE, WARWICK
            "100071512710",  # DARLINGSCOTT HILL, DARLINGSCOTE ROAD, SHIPSTON-ON-STOUR
            "100071244138",  # WIL HAVEN, DARLINGSCOTE ROAD, SHIPSTON-ON-STOUR
            "10023584621",  # DITCHFORD FRIARY MANOR, TIDMINGTON, SHIPSTON-ON-STOUR
            "10023584622",  # GARDEN COTTAGE DITCHFORD FRIARY DITCHFORD ROAD, TIDMINGTON
            "10023584685",  # LITTLE KIRBY, KIRBY FARM, WHATCOTE, SHIPSTON-ON-STOUR
            "100071241496",  # GLENDALE, CAMP LANE, WARMINGTON, BANBURY
            "100071241501",  # RIDGE HOUSE, CAMP LANE, WARMINGTON, BANBURY
            "10023582389",  # EGGE COTTAGE, EDGEHILL, BANBURY
            "10023387192",  # BARN VIEW, KYTE GREEN, HENLEY-IN-ARDEN
            "10094564878",  # FLAT 1 RIVERSIDE LODGE, CLIFFORD MILL, CLIFFORD ROAD, STRATFORD-UPON-AVON
            "10094564879",  # FLAT 2 RIVERSIDE LODGE, CLIFFORD MILL, CLIFFORD ROAD, STRATFORD-UPON-AVON
            "10094564880",  # FLAT 3 RIVERSIDE LODGE, CLIFFORD MILL, CLIFFORD ROAD, STRATFORD-UPON-AVON
            "10094564881",  # FLAT 4 RIVERSIDE LODGE, CLIFFORD MILL, CLIFFORD ROAD, STRATFORD-UPON-AVON
            "10094564882",  # FLAT 5 RIVERSIDE LODGE, CLIFFORD MILL, CLIFFORD ROAD, STRATFORD-UPON-AVON
            "10094564883",  # FLAT 6 RIVERSIDE LODGE, CLIFFORD MILL, CLIFFORD ROAD, STRATFORD-UPON-AVON
            "10023382223",  # RADBROOK EDGE, PRESTON ON STOUR, STRATFORD-UPON-AVON
            "100071244137",  # WHADDON FARM, DARLINGSCOTE ROAD, SHIPSTON-ON-STOUR
            "100071249075",  # GREENFIELDS FARM, HARDWICK LANE, OUTHILL, STUDLEY
            "10023580629",  # OX HOUSE FARM, COMBROOK, WARWICK
            "100071241494",  # BATTLE LODGE, CAMP LANE, WARMINGTON, BANBURY
            "100071241504",  # YENTON, CAMP LANE, WARMINGTON, BANBURY
        ]:
            return None

        if record.addressline6 in [
            "CV36 4DY",  # HIGH SCHOOL BUNGALOW & LOW FURLONG, DARLINGSCOTE ROAD, SHIPSTON-ON-STOUR
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # Chaser Suite, Stratford-upon-Avon Racecourse, Luddington Road
        if record.polling_place_id == "10305":
            record = record._replace(
                polling_place_easting="0", polling_place_northing="0"
            )

        rec = super().station_record_to_dict(record)

        # Alcester Methodist Church, Priory Road, Alcester
        if rec["internal_council_id"] == "10403":
            rec["location"] = Point(-1.871973, 52.214217, srid=4326)

        # Alcester Guide and Scout Centre, 28 Moorfield Road, Alcester
        if rec["internal_council_id"] == "10410":
            rec["location"] = Point(-1.871852, 52.216259, srid=4326)

        return rec
