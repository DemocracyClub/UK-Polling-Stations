from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E08000013"
    addresses_name = "local.2019-05-02/Version 1/Democracy_Club__02May2019helens.tsv"
    stations_name = "local.2019-05-02/Version 1/Democracy_Club__02May2019helens.tsv"
    elections = ["local.2019-05-02"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):
        if record.polling_place_id == "2694":
            record = record._replace(polling_place_postcode="WA12 0NH")
        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "39079909",  # WN57TY -> WN57TX : 83 Carr Mill Road, Billinge,Nr. Wigan,
            "39061437",  # WA128RA -> WA128RP : Alexandra Care Home, Park Road South, Newton-le-Willows,, Merseyside
            "39000688",  # WA104DL -> WA104DN : 49 Alder Hey Road, Eccleston,St Helens,, Merseyside
            "39068718",  # L354PZ -> L354PX : 2 The Orchard, Rainhill, Merseyside
            "39086199",  # WN57PG -> WN57PF : 9A Rainford Road, Billinge,Nr. Wigan,
            "39076000",  # WA118NU -> WA118NT : Ivy Cottage, Ivy Lane, Rainford,St. Helens,, Merseyside
            "39088582",  # WA95HQ -> WA95EP : 322A Elephant Lane, St Helens,, Merseyside
            "39075197",  # WA94HX -> WA94HS : 300 Reginald Road, St Helens,, Merseyside
            "39002933",  # WA102RS -> WA102RL : 40 Baldwin Street, St Helens,, Merseyside
            "39175085",  # WA118RD -> WA118RG : Fir Tree Farmhouse, 54 Pimbo Road, Kings Moss, St. Helens, Merseyside
            "39038634",  # WA104QQ -> WA104QF : Mill Bungalow, Mill Brow, Eccleston,St Helens,, Merseyside
            "39067031",  # WN57TX -> WN57TY : Tan Yard House Farm, Carr Mill Road, Billinge,Nr. Wigan,
            "39068717",  # L354PZ -> L354PX : 1 The Orchard, Rainhill, Merseyside
        ]:
            rec["accept_suggestion"] = True

        if uprn in [
            "39088928",  # WA102NA -> WA102LP : 22 Boundary Road, St Helens,, Merseyside
            "39086246",  # WA118PX -> WA110LA : 144-146 Church Road, Rainford,St. Helens,, Merseyside
            "39095244",  # WA94SD -> WA105RG : 9 Waymark Gardens, St Helens,, Merseyside
            "39091800",  # WA104DS -> WA119TB : 79 Newlove Avenue, St Helens,, Merseyside
            "39093918",  # WA104GA -> WA101JT : 32 Cunningham Court, St Helens,, Merseyside
        ]:
            rec["accept_suggestion"] = False

        return rec
