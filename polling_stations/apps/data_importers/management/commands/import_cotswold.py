from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "COT"
    addresses_name = (
        "2024-07-04/2024-06-13T07:52:47.518892/Democracy_Club__04July2024.tsv"
    )
    stations_name = (
        "2024-07-04/2024-06-13T07:52:47.518892/Democracy_Club__04July2024.tsv"
    )
    elections = ["2024-07-04"]
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
            "10095337476",  # 1 ROOKERY FIELD, WOODMANCOTE, CIRENCESTER
            "10095337477",  # 2 ROOKERY FIELD, WOODMANCOTE, CIRENCESTER
            "10095337478",  # 3 ROOKERY FIELD, WOODMANCOTE, CIRENCESTER
            "10013883801",  # THE STABLES, SOUTH HILL FARM, STATION ROAD, STOW ON THE WOLD, CHELTENHAM
            "10013397276",  # BEDWELL HOUSE, LONDON ROAD, NORTHLEACH, CHELTENHAM
            "10013397991",  # 1 HATHEROP, CIRENCESTER
            "10022834932",  # MANOR FARM, THORNHILL, LECHLADE
            "10022842658",  # SHOOTERS HILL HOUSE ROAD FROM SPRATSGATE LANE TO WEST OF THE BYRE, EWEN
            "10022839178",  # JACKAMENTS FARM, RODMARTON, CIRENCESTER
            "10022839173",  # JACKAMENTS BARN, RODMARTON, CIRENCESTER
            "10022838052",  # THE OLD FORGE, WESTONBIRT, TETBURY
            "10022838048",  # THE BOTHY, WESTONBIRT, TETBURY
            "10024444000",  # BREWERS HOUSE, UPPER RECTORY FARM, DAGLINGWORTH, CIRENCESTER
            "10013397285",  # BEDWELL BARN, LONDON ROAD, NORTHLEACH, CHELTENHAM
            "10024443650",  # BRAMBLE MERE, WHELFORD ROAD, FAIRFORD
            "10093271128",  # DAIRY STORE, TETBURY ROAD, CIRENCESTER
            "100120433154",  # DAIRY COTTAGE, TETBURY ROAD, CIRENCESTER
            "10093268937",  # MOBILE HOME AT WINTER BROOK MAIN ROAD THROUGH LONG NEWNTON, LONG NEWNTON
            "10023476199",  # WINTER BROOK, LONG NEWNTON, TETBURY
            "10095336792",  # HINCHWICK HILL BARN, OLD HINCHWICK, CONDICOTE, CHELTENHAM
            "10006841182",  # ASTON HALE FARM, STRATFORD ROAD, MORETON-IN-MARSH
            "10023478480",  # FIVE ACRE FARM, PEGGLESWORTH, ANDOVERSFORD, CHELTENHAM
            "10022838042",  # EAST LODGE, WESTONBIRT, TETBURY
            "10013392569",  # LYDE COTTAGE, UPPER COBERLEY, CHELTENHAM
            "10022851137",  # PINSWELL ROUND HOUSE A435 COLESBOURNE JUNCTION TO COTT PLANTATION JUNCTION, COLESBOURNE
            "10013397361",  # 1 SPRINGHILL COTTAGES, SPRINGHILL, MORETON-IN-MARSH
        ]:
            return None

        if record.addressline6 in [
            # splits
            "GL54 5US",
            "GL56 9NF",
            "GL55 6LW",
            "GL54 1LT",
            "GL7 3PR",
            "GL7 2LW",
            "GL7 5RA",
            "GL8 8RY",
            "GL54 3ER",
            "GL54 3LX",
            # looks wrong
            "GL54 3QB",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # add point for: St Mary Magdalene Church, Downs Way, Baunton, Cirencester, GL7 7DH
        if record.polling_place_id == "27385":
            record = record._replace(
                polling_place_easting="402181",
                polling_place_northing="204691",
            )

        # add point for: St Mary`s Church, Meysey Hampton, GL7 5JS
        if record.polling_place_id == "27293":
            record = record._replace(
                polling_place_easting="411692",
                polling_place_northing="200044",
            )
        return super().station_record_to_dict(record)
