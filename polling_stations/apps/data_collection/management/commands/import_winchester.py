from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000094"
    addresses_name = "local.2019-05-02/Version 1/Democracy_Club__02May2019Win.tsv"
    stations_name = "local.2019-05-02/Version 1/Democracy_Club__02May2019Win.tsv"
    elections = ["local.2019-05-02"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if uprn == "100062526371":
            rec["postcode"] = "SO322PU"
            rec["accept_suggestion"] = False

        if uprn == "10090844271":
            rec["postcode"] = "PO73AW"
            rec["accept_suggestion"] = False

        if uprn in [
            "200000178418",  # SO240QA -> SO240QT : 166 The Drive, Itchen Stoke, Alresford, Hants
            "100060606091",  # SO212EQ -> SO212HN : Church Lodge, Main Road, Otterbourne, Winchester,Hants
            "200000176579",  # SO322QE -> SO322QF : East Lodge, Holywell, Swanmore, Southampton, Hampshire
            "200000188432",  # SO212BN -> SO212BP : Shawford Park, Shawford, Winchester, Hants
            "200000174990",  # SO321HP -> SO321QF : Little Preshaw Cottage, Preshaw, Upham, Southampton, Hants
            "200000184694",  # SO321JN -> SO321JJ : Barnfield House, White Hill, Upham, Southampton
            "200000176477",  # SO322LB -> SO322LG : 14 Forest Gardens, Waltham Chase, Southampton
            "200000176476",  # SO322LB -> SO322LG : 15 Forest Gardens, Waltham Chase, Southampton
        ]:
            rec["accept_suggestion"] = True

        if uprn in [
            "100060606291",  # SO211QA -> SO211LF : Maytree, Mare Lane, Hazeley, Twyford, Winchester, Hants
            "200000180131",  # SO239BH -> SO230HU : The Garden Flat, 19B Bridge Street, Winchester, Hants
        ]:
            rec["accept_suggestion"] = False

        return rec

    def station_record_to_dict(self, record):

        if record.polling_place_id == "7796":
            record = record._replace(polling_place_easting="452220")
            record = record._replace(polling_place_northing="119570")

        if record.polling_place_id == "7793":
            record = record._replace(polling_place_postcode="SO24 0NA")
        if record.polling_place_id == "7826":
            record = record._replace(polling_place_postcode="SO21 3EW")

        if record.polling_place_id == "7842":
            record = record._replace(polling_place_postcode="SO22 6LB")
        if record.polling_place_id == "7622":
            record = record._replace(polling_place_postcode="SO32 3PA")

        return super().station_record_to_dict(record)
