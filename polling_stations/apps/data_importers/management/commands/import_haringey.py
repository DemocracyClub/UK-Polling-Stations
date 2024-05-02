from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "HRY"
    addresses_name = (
        "2024-05-02/2024-04-09T12:59:07.947391/Democracy_Club__02May2024v2.tsv"
    )
    stations_name = (
        "2024-05-02/2024-04-09T12:59:07.947391/Democracy_Club__02May2024v2.tsv"
    )
    elections = ["2024-05-02"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10022940851",  # 6 HORNSEY PARK ROAD, LONDON
            "10093594285",  # 604 LORDSHIP LANE, LONDON
            "100021236940",  # FIRST FLOOR FLAT 294 WEST GREEN ROAD, TOTTENHAM, LONDON
            "10022939227",  # 398A WEST GREEN ROAD, LONDON
            "100021171953",  # 16 DALBYS CRESCENT, SELBY ROAD, LONDON
            "100023165900",  # 861 HIGH ROAD, TOTTENHAM, LONDON
            # The following UPRNs seem to have the wrong geocoding:
            "100021195610",  # FLAT B 41 LANGHAM ROAD, TOTTENHAM, LONDON
            "100021195611",  # FLAT C 41 LANGHAM ROAD, TOTTENHAM, LONDON
            "100021195622",  # FLAT 3 46 LANGHAM ROAD, TOTTENHAM, LONDON
            "100021195632",  # FLAT A 52 LANGHAM ROAD, TOTTENHAM, LONDON
            "100021195886",  # FIRST FLOOR LEFT FLAT 170-172 LANGHAM ROAD, TOTTENHAM, LONDON
            "100021195887",  # GROUND FLOOR FLAT 170-172 LANGHAM ROAD, TOTTENHAM, LONDON
            "100023151858",  # FLAT A 34 LANGHAM ROAD, TOTTENHAM, LONDON
            "100023151859",  # FLAT B 34 LANGHAM ROAD, TOTTENHAM, LONDON
            "100023151860",  # FLAT C 34 LANGHAM ROAD, TOTTENHAM, LONDON
            "100023151861",  # FLAT D 34 LANGHAM ROAD, TOTTENHAM, LONDON
            "100023151879",  # FLAT B 52 LANGHAM ROAD, TOTTENHAM, LONDON
            "100023151880",  # FLAT C 52 LANGHAM ROAD, TOTTENHAM, LONDON
            "100023152045",  # FLAT A 41 LANGHAM ROAD, TOTTENHAM, LONDON
            "100023152046",  # FLAT A 29 LANGHAM ROAD, TOTTENHAM, LONDON
            "100023152047",  # FLAT B 29 LANGHAM ROAD, TOTTENHAM, LONDON
            "10003983258",  # FIRST FLOOR RIGHT FLAT 170-172 LANGHAM ROAD, TOTTENHAM, LONDON
            "200002046191",  # FLAT 2 46 LANGHAM ROAD, TOTTENHAM, LONDON
            "200002046198",  # FLAT 1 46 LANGHAM ROAD, TOTTENHAM, LONDON
        ]:
            return None
        if record.addressline6 in [
            # split
            "N22 8ET",
            "N17 7AT",
            "N17 6LE",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # bugreport #631
        # remove incorrect coords for: St John Vianney School, Stanley Road, London, N15 3HD
        if record.polling_place_id == "11399":
            record = record._replace(
                polling_place_easting="", polling_place_northing=""
            )

        # Station change requested by council
        # OLD: Earlsmead Primary School, Wakefield Road Entrance, Broad Lane, London, N15 4PW
        # NEW: Earlsmead Primary School, Walton Road Entrance, Broad Lane, London, N15 4PW
        if record.polling_place_id == "11433":
            record = record._replace(polling_place_address_1="Walton Road Entrance")

        return super().station_record_to_dict(record)
