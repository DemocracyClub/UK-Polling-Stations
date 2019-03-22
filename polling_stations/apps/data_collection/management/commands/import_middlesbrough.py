from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E06000002"
    addresses_name = "local.2019-05-02/Version 1/middlesbrough-.tsv"
    stations_name = "local.2019-05-02/Version 1/middlesbrough-.tsv"
    elections = ["local.2019-05-02"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):

        if record.polling_place_id in ["7950", "7849"]:
            record = record._replace(polling_place_easting="0")
            record = record._replace(polling_place_northing="0")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10023173215",  # TS12HJ -> TS12ET : Apartment 1 Central Hall, 108a Borough Road, Middlesbrough
            "10023173216",  # TS12HJ -> TS12ET : Apartment 2 Central Hall, 108a Borough Road, Middlesbrough
            "10023173217",  # TS12HJ -> TS12ET : Apartment 3 Central Hall, 108a Borough Road, Middlesbrough
            "10023173218",  # TS12HJ -> TS12ET : Apartment 4 Central Hall, 108a Borough Road, Middlesbrough
            "10023173219",  # TS12HJ -> TS12ET : Apartment 5 Central Hall, 108a Borough Road, Middlesbrough
            "10023173220",  # TS12HJ -> TS12ET : Apartment 6 Central Hall, 108a Borough Road, Middlesbrough
            "10023173221",  # TS12HJ -> TS12ET : Apartment 7 Central Hall, 108a Borough Road, Middlesbrough
            "10023173222",  # TS12HJ -> TS12ET : Apartment 8 Central Hall, 108a Borough Road, Middlesbrough
            "10023173223",  # TS12HJ -> TS12ET : Apartment 9 Central Hall, 108a Borough Road, Middlesbrough
            "10023173224",  # TS12HJ -> TS12ET : Apartment 10 Central Hall, 108a Borough Road, Middlesbrough
            "10023173225",  # TS12HJ -> TS12ET : Apartment 11 Central Hall, 108a Borough Road, Middlesbrough
            "10023173226",  # TS12HJ -> TS12ET : Apartment 12 Central Hall, 108a Borough Road, Middlesbrough
            "10023173228",  # TS12HJ -> TS12ET : Apartment 14 Central Hall, 108a Borough Road, Middlesbrough
            "10023173229",  # TS12HJ -> TS12ET : Apartment 15 Central Hall, 108a Borough Road, Middlesbrough
            "10023173230",  # TS12HJ -> TS12ET : Apartment 16 Central Hall, 108a Borough Road, Middlesbrough
            "10023173231",  # TS12HJ -> TS12ET : Apartment 17 Central Hall, 108a Borough Road, Middlesbrough
            "10023173232",  # TS12HJ -> TS12ET : Apartment 18 Central Hall, 108a Borough Road, Middlesbrough
            "10023173233",  # TS12HJ -> TS12ET : Apartment 19 Central Hall, 108a Borough Road, Middlesbrough
            "10023173234",  # TS12HJ -> TS12ET : Apartment 20 Central Hall, 108a Borough Road, Middlesbrough
            "10023173235",  # TS12HJ -> TS12ET : Apartment 21 Central Hall, 108a Borough Road, Middlesbrough
            "10023173236",  # TS12HJ -> TS12ET : Apartment 22 Central Hall, 108a Borough Road, Middlesbrough
            "10023173237",  # TS12HJ -> TS12ET : Apartment 23 Central Hall, 108a Borough Road, Middlesbrough
            "10023173238",  # TS12HJ -> TS12ET : Apartment 24 Central Hall, 108a Borough Road, Middlesbrough
            "10023173239",  # TS12HJ -> TS12ET : Apartment 25 Central Hall, 108a Borough Road, Middlesbrough
            "10023173240",  # TS12HJ -> TS12ET : Apartment 26 Central Hall, 108a Borough Road, Middlesbrough
            "10023173241",  # TS12HJ -> TS12ET : Apartment 27 Central Hall, 108a Borough Road, Middlesbrough
            "10023173242",  # TS12HJ -> TS12ET : Apartment 28 Central Hall, 108a Borough Road, Middlesbrough
            "10023173243",  # TS12HJ -> TS12ET : Apartment 29 Central Hall, 108a Borough Road, Middlesbrough
            "10023173244",  # TS12HJ -> TS12ET : Apartment 30 Central Hall, 108a Borough Road, Middlesbrough
            "10023173245",  # TS12HJ -> TS12ET : Apartment 31 Central Hall, 108a Borough Road, Middlesbrough
            "10023173246",  # TS12HJ -> TS12ET : Apartment 32 Central Hall, 108a Borough Road, Middlesbrough
            "10023173247",  # TS12HJ -> TS12ET : Apartment 33 Central Hall, 108a Borough Road, Middlesbrough
            "10023173248",  # TS12HJ -> TS12ET : Apartment 34 Central Hall, 108a Borough Road, Middlesbrough
            "10023173249",  # TS12HJ -> TS12ET : Apartment 35 Central Hall, 108a Borough Road, Middlesbrough
            "10023173250",  # TS12HJ -> TS12ET : Apartment 36 Central Hall, 108a Borough Road, Middlesbrough
            "10023173251",  # TS12HJ -> TS12ET : Apartment 37 Central Hall, 108a Borough Road, Middlesbrough
            "10023173252",  # TS12HJ -> TS12ET : Apartment 38 Central Hall, 108a Borough Road, Middlesbrough
            "10023173253",  # TS12HJ -> TS12ET : Apartment 39 Central Hall, 108a Borough Road, Middlesbrough
            "10023173254",  # TS12HJ -> TS12ET : Apartment 40 Central Hall, 108a Borough Road, Middlesbrough
            "10023173255",  # TS12HJ -> TS12ET : Apartment 41 Central Hall, 108a Borough Road, Middlesbrough
            "10023173256",  # TS12HJ -> TS12ET : Apartment 42 Central Hall, 108a Borough Road, Middlesbrough
            "10023173257",  # TS12HJ -> TS12ET : Apartment 43 Central Hall, 108a Borough Road, Middlesbrough
            "10023173258",  # TS12HJ -> TS12ET : Apartment 44 Central Hall, 108a Borough Road, Middlesbrough
            "10023173259",  # TS12HJ -> TS12ET : Apartment 45 Central Hall, 108a Borough Road, Middlesbrough
            "10023173260",  # TS12HJ -> TS12ET : Apartment 46 Central Hall, 108a Borough Road, Middlesbrough
            "10023173261",  # TS12HJ -> TS12ET : Apartment 47 Central Hall, 108a Borough Road, Middlesbrough
            "10023173262",  # TS12HJ -> TS12ET : Apartment 48 Central Hall, 108a Borough Road, Middlesbrough
            "10023173263",  # TS12HJ -> TS12ET : Apartment 49 Central Hall, 108a Borough Road, Middlesbrough
            "10023173264",  # TS12HJ -> TS12ET : Apartment 50 Central Hall, 108a Borough Road, Middlesbrough
            "10023173265",  # TS12HJ -> TS12ET : Apartment 51 Central Hall, 108a Borough Road, Middlesbrough
            "10023173266",  # TS12HJ -> TS12ET : Apartment 52 Central Hall, 108a Borough Road, Middlesbrough
            "10023173267",  # TS12HJ -> TS12ET : Apartment 53 Central Hall, 108a Borough Road, Middlesbrough
            "10023173268",  # TS12HJ -> TS12ET : Apartment 54 Central Hall, 108a Borough Road, Middlesbrough
            "10023173269",  # TS12HJ -> TS12ET : Apartment 55 Central Hall, 108a Borough Road, Middlesbrough
            "10023173270",  # TS12HJ -> TS12ET : Apartment 56 Central Hall, 108a Borough Road, Middlesbrough
            "10023173271",  # TS12HJ -> TS12ET : Apartment 57 Central Hall, 108a Borough Road, Middlesbrough
            "10023173272",  # TS12HJ -> TS12ET : Apartment 58 Central Hall, 108a Borough Road, Middlesbrough
            "10023173273",  # TS12HJ -> TS12ET : Apartment 59 Central Hall, 108a Borough Road, Middlesbrough
            "10023173274",  # TS12HJ -> TS12ET : Apartment 60 Central Hall, 108a Borough Road, Middlesbrough
            "10023173275",  # TS12HJ -> TS12ET : Apartment 61 Central Hall, 108a Borough Road, Middlesbrough
            "10023173276",  # TS12HJ -> TS12ET : Apartment 62 Central Hall, 108a Borough Road, Middlesbrough
            "10023173277",  # TS12HJ -> TS12ET : Apartment 63 Central Hall, 108a Borough Road, Middlesbrough
            "10023173278",  # TS12HJ -> TS12ET : Apartment 64 Central Hall, 108a Borough Road, Middlesbrough
            "10023173279",  # TS12HJ -> TS12ET : Apartment 65 Central Hall, 108a Borough Road, Middlesbrough
            "10023173280",  # TS12HJ -> TS12ET : Apartment 66 Central Hall, 108a Borough Road, Middlesbrough
            "10023173281",  # TS12HJ -> TS12ET : Apartment 67 Central Hall, 108a Borough Road, Middlesbrough
            "10023173282",  # TS12HJ -> TS12ET : Apartment 68 Central Hall, 108a Borough Road, Middlesbrough
            "10023173283",  # TS12HJ -> TS12ET : Apartment 69 Central Hall, 108a Borough Road, Middlesbrough
            "10023173284",  # TS12HJ -> TS12ET : Apartment 70 Central Hall, 108a Borough Road, Middlesbrough
            "10023173285",  # TS12HJ -> TS12ET : Apartment 71 Central Hall, 108a Borough Road, Middlesbrough
            "10023173286",  # TS12HJ -> TS12ET : Apartment 72 Central Hall, 108a Borough Road, Middlesbrough
            "10023173287",  # TS12HJ -> TS12ET : Apartment 73 Central Hall, 108a Borough Road, Middlesbrough
            "10023173288",  # TS12HJ -> TS12ET : Apartment 74 Central Hall, 108a Borough Road, Middlesbrough
            "10023173289",  # TS12HJ -> TS12ET : Apartment 75 Central Hall, 108a Borough Road, Middlesbrough
            # Google route very odd but start an end correct.
            "200001936013",  # TS89EH -> TS89DW : Coulby Manor Cottage, Ladgate Lane, Middlesbrough
            "10093978033",  # TS43BS -> TS43SE : Flat Above Toby Cavery, Marton Road, Middlesbrough
            "100110677272",  # TS78PA -> TS78NX : Brockendale, Dixons Bank, Middlesbrough
            "100110092822",  # TS14PE -> TS14PX : Flat A, 150 Ayresome Street, Middlesbrough
            "10023181141",  # TS56BA -> TS56JS : 21B St. Barnabas Road, Linthorpe, Middlesbrough
            "10023181142",  # TS56BA -> TS56JS : 21C St. Barnabas Road, Linthorpe, Middlesbrough
            "100110136300",  # TS56JS -> TS56AT : 33A St. Barnabas Road, Linthorpe, Middlesbrough
            "100110789156",  # TS56JS -> TS56AT : 33B St. Barnabas Road, Linthorpe, Middlesbrough
            "100110678394",  # TS89LX -> TS89DF : The Bungalow, The Unicorn Centre, Stainton Way, Middlesbrough
        ]:
            rec["accept_suggestion"] = True

        return rec
