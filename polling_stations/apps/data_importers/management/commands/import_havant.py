from data_importers.management.commands import BaseXpressWebLookupCsvImporter

STATION_LOCATIONS = {
    "7295": {  # St Andrews Church Hall, Havant Road, Farlington, PO6 1AA
        "easting": "468574",
        "northing": "105820",
    },
    "7308": {  # Bedhampton Community Centre, 21 Bedhampton Road, Bedhampton, PO9 3ES
        "easting": "470631",
        "northing": "106563",
    },
    "7300": {  # Barncroft Primary School, Park Lane, PO9 3HN
        "easting": "470525",
        "northing": "107515",
    },
    "7304": {  # St Joseph's Church Hall, 134 West Street, Havant, PO9 1LP
        "easting": "471198",
        "northing": "106452",
    },
    "7311": {  # Westbrook Hall, Grassmere Way, Waterlooville, PO7 8NU
        "easting": "469907",
        "northing": "110222",
    },
    "7315": {  # Cowplain Activity Centre, Padnell Road, Cowplain, PO8 8EH
        "easting": "469611",
        "northing": "110975",
    },
    "7319": {  # Cowplain Social Club, 54 London Road, Cowplain, PO8 8EN
        "easting": "469290",
        "northing": "111259",
    },
    "7323": {  # Sports Pavilion, Hollybank Recreation Ground, Southleigh Road, PO10 7TX
        "easting": "474660",
        "northing": "107295",
    },
    "7327": {  # 1st Emsworth Scout Hut, Conigar Road, Emsworth, PO10 7SZ
        "easting": "474945",
        "northing": "107336",
    },
    "7330": {  # Emsworth Primary School, Victoria Road, Emsworth, PO10 7LX
        "easting": "474174",
        "northing": "106337",
    },
    "7333": {  # Small Auditorium, Emsworth Baptist Church, Emsworth Baptist Church, PO10 7BY
        "easting": "474948",
        "northing": "105929",
    },
    "7336": {  # The Slipper Room, Brookfield Hotel, 93 - 95 Havant Road, PO10 7LF
        "easting": "473702",
        "northing": "106022",
    },
    "7339": {  # Hart Plain Church, 59 Hart Plain Avenue, PO10 7LF
        "easting": "468071",
        "northing": "111006",
    },
    "7348": {  # Woodcroft Primary School, 37 Woodcroft Lane, Lovedean, PO8 9QG
        "easting": "468593",
        "northing": "112084",
    },
    "7352": {  # Wecock Community Association, The Acorn Centre, 3 The Kestrels, PO8 9UB
        "easting": "468216",
        "northing": "111751",
    },
    "7355": {  # North Hayling Recreation Hall, St Peters Road, PO11 0RT
        "easting": "473110",
        "northing": "103049",
    },
    "7359": {  # Royal British Legion Hall, Legion Road, Hayling Island, PO11 9ES
        "easting": "472254",
        "northing": "99767",
    },
    "7363": {  # St Andrews Church Hall, 1 - 3 Culver Drive, Off Southwood Rd, PO11 9QL
        "easting": "473268",
        "northing": "98517",
    },
    "7366": {  # Eastoke Community Centre, Wheatlands Avenue, Hayling Island, PO11 9SG
        "easting": "474003",
        "northing": "98272",
    },
    "7369": {  # Portakabin, Between 11/12 Island Close, via New Cut, PO11 0NA
        "easting": "471996",
        "northing": "103327",
    },
    "7372": {  # United Reformed Church, Hollow Lane, Hayling Island, PO11 9EY
        "easting": "472175",
        "northing": "99196",
    },
    "7375": {  # Hayling Island Community Centre, Station Road, PO11 OHB
        "easting": "471235",
        "northing": "99451",
    },
    "7378": {  # Hampshire Rose, 44 London Road, Widley, PO7 5AG
        "easting": "467032",
        "northing": "106977",
    },
    "7382": {  # Phoenix Community Centre, 84 London Road, Crookhorn, PO7 5QB
        "easting": "468470",
        "northing": "107206",
    },
    "7385": {  # The Purbrook Centre, Stakes Road, PO7 5LX
        "easting": "467385",
        "northing": "107939",
    },
    "7388": {  # The Pallant Centre, The Pallant, Havant, PO9 1BE
        "easting": "471908",
        "northing": "106307",
    },
    "7392": {  # HYSTS Building, The Ship Inn Car Park, Langstone Road, PO9 1RD
        "easting": "471860",
        "northing": "104729",
    },
    "7396": {  # Warblington School, Southleigh Road, PO9 2RR
        "easting": "472664",
        "northing": "106454",
    },
    "7400": {  # The Stride Centre, Daffodil Way, Denvilles, PO9 2FA
        "easting": "473300",
        "northing": "106931",
    },
    "7407": {  # Springwood Community Building, 110 Springwood Avenue, Waterlooville, PO7 8BJ
        "easting": "468956",
        "northing": "108664",
    },
    "7403": {  # Windsor Court, Anne Crescent, Waterlooville, PO7 7NA
        "easting": "468503",
        "northing": "108660",
    },
    "7411": {  # Growing Places, Mill Hill Primary School, Mill Road, PO7 7DB
        "easting": "468076",
        "northing": "108770",
    },
    "7415": {  # Crookhorn College, Stakes Hill Road, Waterlooville, PO7 5UD
        "easting": "468700",
        "northing": "107849",
    },
    "7418": {  # Queens Inclosure Primary School, Cornelius Drive, Waterlooville, PO7 8NT
        "easting": "469459",
        "northing": "110272",
    },
    "7421": {  # Waterlooville Baptist Church, 368 London Road, Waterlooville, PO7 7SY
        "easting": "468568",
        "northing": "109922",
    },
    "7425": {  # St Georges Church Hall, St Georges Walk, PO7 7EH
        "easting": "468120",
        "northing": "109444",
    },
    "7467": {  # Scout Hall, 1st Hart Plain Scout Group, 105/107 Milton Road, PO7 6AG
        "easting": "468029",
        "northing": "110627",
    },
}


class Command(BaseXpressWebLookupCsvImporter):
    council_id = "HAA"
    addresses_name = "2023-05-04/2023-03-16T14:48:52.200029/PropertyPostCodePollingStationWebLookup-2023-03-16.TSV"
    stations_name = "2023-05-04/2023-03-16T14:48:52.200029/PropertyPostCodePollingStationWebLookup-2023-03-16.TSV"
    elections = ["2023-05-04"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "10013683413",  # 47 WELLESLEY COURT, DARNEL ROAD, WATERLOOVILLE
        ]:
            return None
        if record.postcode in [
            "PO11 9LA",
            "PO8 9UB",
            "PO10 7HN",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        if location := STATION_LOCATIONS.get(record.pollingplaceid, None):
            record = record._replace(
                pollingplaceeasting=location["easting"],
                pollingplacenorthing=location["northing"],
            )

        return super().station_record_to_dict(record)
