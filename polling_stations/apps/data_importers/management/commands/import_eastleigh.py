from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter
from django.contrib.gis.geos import Point


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "EAT"
    addresses_name = (
        "2023-05-04/2023-03-02T10:58:53.156539/Democracy_Club__04May2023.tsv"
    )
    stations_name = (
        "2023-05-04/2023-03-02T10:58:53.156539/Democracy_Club__04May2023.tsv"
    )
    elections = ["2023-05-04"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "200002902856",  # FLAT, 2 WINCHESTER ROAD, CHANDLER'S FORD, EASTLEIGH
            "10091134664",  # CHERRYWOOD, LOWFORD HILL, BURSLEDON, SOUTHAMPTON
            "10091134663",  # LARCHWOOD, LOWFORD HILL, BURSLEDON, SOUTHAMPTON
            "10091134662",  # ASHWOOD, LOWFORD HILL, BURSLEDON, SOUTHAMPTON
            "10009640001",  # OAK COTTAGE, ALLINGTON LANE, FAIR OAK, EASTLEIGH
            "10091134661",  # SPINDLEWOOD, LOWFORD HILL, BURSLEDON, SOUTHAMPTON
            "10094386469",  # THE HOUND WB02, SATCHELL LANE, HAMBLE, SOUTHAMPTON
            "100060324530",  # POND FARM, MORTIMERS LANE, UPHAM, SOUTHAMPTON
        ]:
            return None

        if record.addressline6 in [
            # splits
            "SO31 8AF",
            "SO53 2FG",
            "SO50 6RQ",  # 1 - 2 CHICKENHALL COTTAGES, CHICKENHALL LANE, EASTLEIGH
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # Abbey Hall Victoria Road Netley Abbey Southampton SO31 5FA
        if record.polling_place_id == "5722":
            record = record._replace(
                polling_place_easting="445235", polling_place_northing="108734"
            )

        # Chandler's Ford Community Centre, Hursley Road, Chandler's Ford, Eastleigh, SO53 2FS
        if record.polling_place_id == "5709":
            record = record._replace(polling_place_postcode="SO53 2FT")

        rec = super().station_record_to_dict(record)

        # Chandler's Ford Central Club & Institute, Winchester Road, Chandler's Ford, Eastleigh
        if rec["internal_council_id"] == "5715":
            rec["location"] = Point(-1.382289, 50.982011, srid=4326)

        # The Hilt, Hiltingbury Recreation Ground, Hiltingbury Road, Chandler's Ford, Eastleigh
        if rec["internal_council_id"] == "5751":
            rec["location"] = Point(-1.385740, 50.997417, srid=4326)

        return rec
