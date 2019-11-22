from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E09000025"
    addresses_name = (
        "parl.2019-12-12/Version 1/LBNewhamDemocracy_Club__12December2019.TSV"
    )
    stations_name = (
        "parl.2019-12-12/Version 1/LBNewhamDemocracy_Club__12December2019.TSV"
    )
    elections = ["parl.2019-12-12"]
    csv_delimiter = "\t"
    allow_station_point_from_postcode = False

    def station_record_to_dict(self, record):
        # Fix from: 890908:polling_stations/apps/data_collection/management/commands/misc_fixes.py:224
        # Carpenters and Docklands Centre 98 Gibbins Road Stratford London
        if record.polling_place_id == "4823":
            record = record._replace(polling_place_easting="538526.11")
            record = record._replace(polling_place_northing="184252.81")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if uprn == "46003425":
            return None  # in an otherwise multiple station postcode, so safe to remove

        if uprn == "10008988958":  # Right property; wrong postcode
            rec["postcode"] = "E162LL"  # was E164LL
            rec["accept_suggestion"] = False

        if uprn == "10094371250":  # Right property; wrong postcode
            rec["postcode"] = "E125AD"  # was E126AD
            rec["accept_suggestion"] = False

        if uprn in [
            "10009004801",  # E78BS -> E78AB : 386A Romford Road, London
            "10009009060",  # E151SL -> E151SH : School House, Gurney Road, London
            "10008984571",  # E154DY -> E153HU : The Angel Inn Public House, 21 Church Street, London
            "10012835081",  # E139ER -> E139PJ : 772 Barking Road, London
            "10090756946",  # E78AW -> E79AW : 36C Earlham Grove, London
            "10090758259",  # E63JE -> E66JE : 28 Buterfly Court, 1 Elderberry Way, London
            "10090758260",  # E63JE -> E66JE : 29 Butterly Court, 1 Elderberry Way, London
            "10034509102",  # E66AQ -> E66HE : Ground Floor Flat, 178 Charlemont Road, London
            "10008987564",  # E126TH -> E126TJ : 459A High Street North, London
            "10009014196",  # E78AR -> E79AR : Basement Flat, 84 Earlham Grove, London
        ]:
            rec["accept_suggestion"] = True

        if uprn in [
            "10023995207",  # E164EB -> E138NE : 301 Newham Way, London
            "10090323539",  # E78NL -> E78QJ : 93 Stafford Road, London
            "10008983114",  # E62BU -> E62BX : 84 Altmore Avenue, London
            "10008988958",  # Right property; wrong postcode
            # Right property, wrong postcode
            "10034508484",  # E66DQ -> E61DQ : Flat Above, 33 Vicarage Lane, London
            "10009012905",  # E163DZ -> E163BZ : Ground Floor Flat, 62A Tree Road, London
        ]:
            rec["accept_suggestion"] = False

        return rec
