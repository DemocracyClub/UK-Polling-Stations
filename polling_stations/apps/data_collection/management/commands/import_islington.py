from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter
from django.contrib.gis.geos import Point


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E09000019"
    addresses_name = "2020-02-24T10:32:45.264757/islington.gov.uk-1582275913000-.TSV"
    stations_name = "2020-02-24T10:32:45.264757/islington.gov.uk-1582275913000-.TSV"
    elections = ["2020-05-07"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if uprn == "10012788158":
            rec["postcode"] = "EC1V 0ET"

        if uprn in [
            "10093624258",  # N79HL -> N79PL : Flat 1 Jewel House, 5 Sterling Way, London
            "10093624259",  # N79HL -> N79PL : Flat 2 Jewel House, 5 Sterling Way, London
            "10093624260",  # N79HL -> N79PL : Flat 3 Jewel House, 5 Sterling Way, London
            "10093624261",  # N79HL -> N79PL : Flat 4 Jewel House, 5 Sterling Way, London
            "10093624262",  # N79HL -> N79PL : Flat 5 Jewel House, 5 Sterling Way, London
            "10093624263",  # N79HL -> N79PL : Flat 6 Jewel House, 5 Sterling Way, London
            "10093624264",  # N79HL -> N79PL : Flat 7 Jewel House, 5 Sterling Way, London
            "10093624265",  # N79HL -> N79PL : Flat 8 Jewel House, 5 Sterling Way, London
            "10093624266",  # N79HL -> N79PL : Flat 9 Jewel House, 5 Sterling Way, London
            "10093624267",  # N79HL -> N79PL : Flat 10 Jewel House, 5 Sterling Way, London
            "10093624268",  # N79HL -> N79PL : Flat 11 Jewel House, 5 Sterling Way, London
            "10093624269",  # N79HL -> N79PL : Flat 12 Jewel House, 5 Sterling Way, London
            "10093624270",  # N79HL -> N79PL : Flat 13 Jewel House, 5 Sterling Way, London
            "10093624271",  # N79HL -> N79PL : Flat 14 Jewel House, 5 Sterling Way, London
            "10093624272",  # N79HL -> N79PL : Flat 15 Jewel House, 5 Sterling Way, London
            "10093624273",  # N79HL -> N79PL : Flat 16 Jewel House, 5 Sterling Way, London
            "10093624274",  # N79HL -> N79PL : Flat 17 Jewel House, 5 Sterling Way, London
            "10093624275",  # N79HL -> N79PL : Flat 18 Jewel House, 5 Sterling Way, London
            "10093624276",  # N79HL -> N79PL : Flat 19 Jewel House, 5 Sterling Way, London
            "10093624277",  # N79HL -> N79PL : Flat 20 Jewel House, 5 Sterling Way, London
            "10093624278",  # N79HL -> N79PL : Flat 21 Jewel House, 5 Sterling Way, London
            "10093624279",  # N79HL -> N79PL : Flat 22 Jewel House, 5 Sterling Way, London
            "10093624280",  # N79HL -> N79PL : Flat 23 Jewel House, 5 Sterling Way, London
            "10093624281",  # N79HL -> N79PL : Flat 24 Jewel House, 5 Sterling Way, London
            "10093624282",  # N79HL -> N79PL : Flat 25 Jewel House, 5 Sterling Way, London
            "10093624283",  # N79HL -> N79PL : Flat 26 Jewel House, 5 Sterling Way, London
            "10093624284",  # N79HL -> N79PL : Flat 27 Jewel House, 5 Sterling Way, London
            "10093624285",  # N79HL -> N79PL : Flat 28 Jewel House, 5 Sterling Way, London
            "10093624286",  # N79HL -> N79PL : Flat 29 Jewel House, 5 Sterling Way, London
            "10093624287",  # N79HL -> N79PL : Flat 30 Jewel House, 5 Sterling Way, London
            "10093624288",  # N79HL -> N79PL : Flat 31 Jewel House, 5 Sterling Way, London
            "10093624289",  # N79HL -> N79PL : Flat 32 Jewel House, 5 Sterling Way, London
            "10093624290",  # N79HL -> N79PL : Flat 33 Jewel House, 5 Sterling Way, London
            "10093624291",  # N79HL -> N79PL : Flat 34 Jewel House, 5 Sterling Way, London
            "10093624292",  # N79HL -> N79PL : Flat 35 Jewel House, 5 Sterling Way, London
            "10093624293",  # N79HL -> N79PL : Flat 36 Jewel House, 5 Sterling Way, London
            "10093624294",  # N79HL -> N79PL : Flat 37 Jewel House, 5 Sterling Way, London
            "10093624295",  # N79HL -> N79PL : Flat 38 Jewel House, 5 Sterling Way, London
            "10093624296",  # N79HL -> N79PL : Flat 39 Jewel House, 5 Sterling Way, London
            "10093624297",  # N79HL -> N79PL : Flat 40 Jewel House, 5 Sterling Way, London
            "10093624298",  # N79HL -> N79PL : Flat 41 Jewel House, 5 Sterling Way, London
            "10093624299",  # N79HL -> N79PL : Flat 42 Jewel House, 5 Sterling Way, London
            "10093624300",  # N79HL -> N79PL : Flat 43 Jewel House, 5 Sterling Way, London
            "10093624301",  # N79HL -> N79PL : Flat 44 Jewel House, 5 Sterling Way, London
            "10093624302",  # N79HL -> N79PL : Flat 45 Jewel House, 5 Sterling Way, London
            "10093624303",  # N79HL -> N79PL : Flat 46 Jewel House, 5 Sterling Way, London
            "10093624304",  # N79HL -> N79PL : Flat 47 Jewel House, 5 Sterling Way, London
            "10093624305",  # N79HL -> N79PL : Flat 48 Jewel House, 5 Sterling Way, London
            "10093624306",  # N79HL -> N79PL : Flat 49 Jewel House, 5 Sterling Way, London
            "10093624307",  # N79HL -> N79PL : Flat 50 Jewel House, 5 Sterling Way, London
            "10093624308",  # N79HL -> N79PL : Flat 51 Jewel House, 5 Sterling Way, London
            "10093624309",  # N79HL -> N79PL : Flat 52 Jewel House, 5 Sterling Way, London
            "10093624310",  # N79HL -> N79PL : Flat 53 Jewel House, 5 Sterling Way, London
            "10093624311",  # N79HL -> N79PL : Flat 54 Jewel House, 5 Sterling Way, London
            "10093624312",  # N79HL -> N79PL : Flat 55 Jewel House, 5 Sterling Way, London
            "10093624313",  # N79HL -> N79PL : Flat 56 Jewel House, 5 Sterling Way, London
            "10093624314",  # N79HL -> N79PL : Flat 57 Jewel House, 5 Sterling Way, London
            "10093624315",  # N79HL -> N79PL : Flat 58 Jewel House, 5 Sterling Way, London
        ]:
            rec["accept_suggestion"] = True
        return rec

    def station_record_to_dict(self, record):
        rec = super().station_record_to_dict(record)

        if rec["internal_council_id"] == "1928":  #    St. Thomas` Church Hall
            rec["location"] = Point(-0.104049, 51.560139, srid=4326)

        if rec["internal_council_id"] == "1916":  # St Joan of Arc Community Centre
            rec["location"] = Point(-0.0966823, 51.5559102, srid=4326)

        if rec["internal_council_id"] == "1934":  # Aubert Court Community Centre.
            rec["location"] = Point(-0.102306, 51.556435, srid=4326)

        return rec
