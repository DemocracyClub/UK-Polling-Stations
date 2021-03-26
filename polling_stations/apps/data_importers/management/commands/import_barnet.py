from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "BNE"
    addresses_name = "2021-03-25T11:42:15.781785/Democracy Club_Polling Districts.csv"
    stations_name = "2021-03-25T11:42:15.781785/Democracy Club_Polling Stations.csv"
    elections = ["2021-05-06"]

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")
        if record.postcode.strip() in [
            "NW7 4SB",
            "HA8 7LZ",
            "N11 3DD",
            "EN4 8QZ",
            "NW11 7ND",
        ]:
            return None

        if uprn in [
            "10091038621",  # FLAT 1 129 HENDON WAY, LONDON
            "10091038625",  # FLAT 5 129 HENDON WAY, LONDON
            "10091038623",  # FLAT 3 129 HENDON WAY, LONDON
            "10091041237",  # FLAT 3, 238 EAST BARNET ROAD, BARNET
            "10091041238",  # FLAT 4, 238 EAST BARNET ROAD, BARNET
            "200163833",  # FLAT 1 41 THE GROVE, FINCHLEY, LONDON
            "200163834",  # FLAT 2 41 THE GROVE, FINCHLEY, LONDON
            "200163838",  # FLAT 6 41 THE GROVE, FINCHLEY, LONDON
            "200196535",  # 1 NINA WALK, LONDON, N20 0RB
        ]:
            return None

        return super().address_record_to_dict(record)
