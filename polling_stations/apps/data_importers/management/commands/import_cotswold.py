from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "COT"
    addresses_name = (
        "2025-05-01/2025-03-10T12:04:49.155852/Democracy_Club__01May2025.tsv"
    )
    stations_name = (
        "2025-05-01/2025-03-10T12:04:49.155852/Democracy_Club__01May2025.tsv"
    )
    elections = ["2025-05-01"]
    csv_encoding = "windows-1252"
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if (
            uprn
            in [
                "10022838989",  # CORNER COTTAGE, TRULL, TETBURY
                "10023475981",  # SELWORTHY, MORETON ROAD, STOW ON THE WOLD, CHELTENHAM
                "10013878640",  # BARTON MEADOW LODGE, GUITING POWER, CHELTENHAM
                "200002916722",  # THE FIRS, NORTHWICK PARK, BLOCKLEY, MORETON-IN-MARSH
                "10095336266",  # GALLOP BOTTOM, GRANGE HILL, NAUNTON, CHELTENHAM
                "10013886740",  # THE STABLE FLAT HARTLEY FARM HARTLEY LANE, LECKHAMPTON HILL, COBERLEY
                "10013886813",  # HARTLEY FARM, HARTLEY LANE, LECKHAMPTON HILL, CHELTENHAM
                "10013883801",  # THE STABLES, SOUTH HILL FARM, STATION ROAD, STOW ON THE WOLD, CHELTENHAM
                "10013397276",  # BEDWELL HOUSE, LONDON ROAD, NORTHLEACH, CHELTENHAM
                "10022838052",  # THE OLD FORGE, WESTONBIRT, TETBURY
                "10022838048",  # THE BOTHY, WESTONBIRT, TETBURY
                "10024444000",  # BREWERS HOUSE, UPPER RECTORY FARM, DAGLINGWORTH, CIRENCESTER
                "10013397285",  # BEDWELL BARN, LONDON ROAD, NORTHLEACH, CHELTENHAM
                "10093271128",  # DAIRY STORE, TETBURY ROAD, CIRENCESTER
                "100120433154",  # DAIRY COTTAGE, TETBURY ROAD, CIRENCESTER
                "10093268937",  # MOBILE HOME AT WINTER BROOK MAIN ROAD THROUGH LONG NEWNTON, LONG NEWNTON
                "10023476199",  # WINTER BROOK, LONG NEWNTON, TETBURY
            ]
        ):
            return None

        if record.addressline6 in [
            # splits
            "GL54 1LT",
            "GL55 6LW",
            "GL54 5US",
            "GL56 9NF",
            "GL7 3PR",
            "GL7 5RA",
            "GL54 3LX",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # # add point for: St Mary Magdalene Church, Downs Way, Baunton, Cirencester, GL7 7DH
        if record.polling_place_id == "30287":
            record = record._replace(
                polling_place_easting="402181",
                polling_place_northing="204691",
            )

        # # add point for: St Mary`s Church, Meysey Hampton, GL7 5JS
        if record.polling_place_id == "30410":
            record = record._replace(
                polling_place_easting="411692",
                polling_place_northing="200044",
            )
        return super().station_record_to_dict(record)
