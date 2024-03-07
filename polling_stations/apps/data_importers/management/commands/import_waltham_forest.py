from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "WFT"
    addresses_name = (
        "2024-05-02/2024-03-12T11:46:31.713315/Democracy_Club__02May2024.tsv"
    )
    stations_name = (
        "2024-05-02/2024-03-12T11:46:31.713315/Democracy_Club__02May2024.tsv"
    )
    elections = ["2024-05-02"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10009149436",  # 24 PENNANT TERRACE, LONDON
            "10024418210",  # 5A ELY ROAD, LONDON
            "10024421904",  # FLAT B 372-374 HIGH ROAD LEYTON, LEYTON, E10 6QE
            "100022981619",  # 27 PENNANT TERRACE, LONDON
            "200001416768",  # 24B COURTENAY ROAD, LEYTONSTONE
            "200001448154",  # SECOND FLOOR FLAT 7A ST JAMES STREET, WALTHAMSTOW
            "10091184386",  # SECOND FLOOR FLAT 32 ST JAMES STREET, WALTHAMSTOW
            "10091184385",  # FIRST FLOOR REAR FLAT 32 ST JAMES STREET, WALTHAMSTOW
            "10091184384",  # FIRST FLOOR FRONT FLAT 32 ST JAMES STREET, WALTHAMSTOW
            "100022580513",  # 41 RINGWOOD ROAD, LONDON
            "100022962188",  # COMMUNITY BASED HOUSING ASSOCIATION, 433-443 HIGH ROAD LEYTONSTONE, LONDON
            "100022961205",  # 1A SELBY ROAD, LEYTONSTONE
            "100022961206",  # 1B SELBY ROAD, LEYTONSTONE
            "200001418558",  # 2 FOREST ROAD, LONDON
            "100022590251",  # 1A THE RIDGEWAY, LONDON
            "100022590253",  # 1C THE RIDGEWAY, LONDON
            "100022590252",  # 1B THE RIDGEWAY, LONDON
            "200001433409",  # 22 MANSFIELD HILL, LONDON
        ]:
            return None

        if record.addressline6 in [
            # splits
            "E4 9DP",
            "E17 7EA",
            "E17 4ED",
            "E11 3DT",
            "E17 5JY",
            "E17 3NL",
            "E17 3DA",
            "E17 3DU",
            # looks wrong
            "E17 6QA",
            "E10 6ES",
            "E11 1LJ",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # more accurate point for: Mission Grove (South Site), Edinburgh Road, Walthamstow, London, E17 8QB
        if record.polling_place_id == "6393":
            record = record._replace(polling_place_easting="536937")
            record = record._replace(polling_place_northing="188842")

        # adding postcode for: YMCA, 642 Forest Road, Walthamstow, London
        if record.polling_place_id == "6299":
            record = record._replace(polling_place_postcode="E17 3EF")

        return super().station_record_to_dict(record)
