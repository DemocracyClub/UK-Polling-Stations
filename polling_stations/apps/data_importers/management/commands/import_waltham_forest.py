from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "WFT"
    addresses_name = (
        "2022-05-05/2022-03-09T16:58:40.436212/Democracy_Club__05May2022.tsv"
    )
    stations_name = (
        "2022-05-05/2022-03-09T16:58:40.436212/Democracy_Club__05May2022.tsv"
    )
    elections = ["2022-05-05"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10009149436",  # 24 PENNANT TERRACE, LONDON
            "10024418210",  # 5A ELY ROAD, LONDON
            "10024421904",  # FLAT B 372-374 HIGH ROAD LEYTON, LEYTON, E10 6QE
            "200001425453",  # 112 FARMILO ROAD, LONDON
            "200001425453",  # GROUND FLOOR FLAT 1 27 QUEENS ROAD, LEYTONSTONE
            "100022517750",  # 316C LEA BRIDGE ROAD, LONDON
            "100023696171",  # 3 OAKLANDS, 37 WEST AVENUE, LONDON
            "10009143272",  # FLAT 1, 58 BORTHWICK ROAD, LONDON
            "100022597338",  # FLAT 5 85 WHIPPS CROSS ROAD, LEYTONSTONE
        ]:
            return None

        if record.addressline6 in [
            "E17 7EA",
            "E17 6HT",
            "E17 3DU",
            "E17 4ED",
            "E17 4PE",
            "E17 5JY",
            "E17 3NL",
            "E11 3DT",
            "E4 9DP",
            "E17 3DA",
            "E11 3PY",
            "E10 5PW",
            "E11 1LJ",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # Mission Grove (South Site) 108 Edinburgh Road Walthamstow London E17 7QB
        if record.polling_place_id == "5968":
            record = record._replace(polling_place_easting="536937")
            record = record._replace(polling_place_northing="188842")

        return super().station_record_to_dict(record)
