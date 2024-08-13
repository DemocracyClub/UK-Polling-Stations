from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "SBU"
    addresses_name = "2021-03-18T18:05:00.006119/Bucks_dedupe.tsv"
    stations_name = "2021-03-18T18:05:00.006119/Bucks_dedupe.tsv"
    elections = ["2021-05-06"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if (
            uprn
            in [
                "10090191083",  # 1 LATCHMOOR WAY, CHALFONT ST. PETER, GERRARDS CROSS
                "10095500760",  # FLAT 1, ORCHE HILL CHAMBERS, 52 PACKHORSE ROAD, GERRARDS CROSS
                "10090191260",  # TWIN OAKS, OXFORD ROAD, GERRARDS CROSS
                "10003242246",  # 41 WINDSOR ROAD, GERRARDS CROSS
                "10003242624",  # 57 PENN ROAD, BEACONSFIELD
                "10090189602",  # GORSEWOOD, TEMPLEWOOD LANE, FARNHAM COMMON, SLOUGH
                "10090192931",  # MOBILE HOME AT STABLES AND PADDOCK WILLETTS LANE, DENHAM
                "10003446603",  # WOODHILL FARM, OXFORD ROAD, GERRARDS CROSS
            ]
        ):
            return None

        if record.addressline6 in ["SL0 0AF", "SL9 7BZ"]:
            return None

        return super().address_record_to_dict(record)
