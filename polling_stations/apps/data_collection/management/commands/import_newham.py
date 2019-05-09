from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E09000025"
    addresses_name = "europarl.2019-05-23/Version 1/Democracy_Club__23May2019Newham.tsv"
    stations_name = "europarl.2019-05-23/Version 1/Democracy_Club__23May2019Newham.tsv"
    elections = ["europarl.2019-05-23"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):
        # Fix from: 890908:polling_stations/apps/data_collection/management/commands/misc_fixes.py:224
        if record.polling_place_id == "4483":
            record = record._replace(polling_place_easting="538526.11")
            record = record._replace(polling_place_northing="184252.81")

        if record.polling_place_id == "4234":
            record = record._replace(polling_place_name="Sandringham Primary School")
            record = record._replace(polling_place_address_1="Sandringham Road")
            record = record._replace(polling_place_address_2="Forest Gate")
            record = record._replace(polling_place_address_3="London")
            record = record._replace(polling_place_address_4="")
            record = record._replace(polling_place_postcode="E7 8ED")
            record = record._replace(polling_place_uprn="")
            record = record._replace(polling_place_easting="0")
            record = record._replace(polling_place_northing="0")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if uprn == "46003425":
            rec["postcode"] = "E62LN"
            rec["accept_suggestion"] = False

        if uprn in [
            "10009004801",  # E78BS -> E78AB : 386A Romford Road, London
            "10034508484",  # E66DQ -> E61DQ : Flat Above, 33 Vicarage Lane, London
            "10034508521",  # E154PT -> E154SA : 34 West Ham Lane, London
            "10009009060",  # E151SL -> E151SH : School House, Gurney Road, London
            "10008984571",  # E154DY -> E153HU : The Angel Inn Public House, 21 Church Street, London
            "10012835081",  # E139ER -> E139PJ : 772 Barking Road, London
            "10009012905",  # E163DZ -> E163BZ : Ground Floor Flat, 62A Tree Road, London
            "10090756946",  # E78AW -> E79AW : 36C Earlham Grove, London
            "10090758259",  # E63JE -> E66JE : 28 Buterfly Court, 1 Elderberry Way, London
            "10090758260",  # E63JE -> E66JE : 29 Butterly Court, 1 Elderberry Way, London
            "10009016787",  # E163RD -> E65QJ : The Lodge The Stables, Stansfeld Road, London
            "10034509102",  # E66AQ -> E66HE : Ground Floor Flat, 178 Charlemont Road, London
            "10008988958",  # E164LL -> E162LL : 8, Woodman Parade, London
        ]:
            rec["accept_suggestion"] = True

        if uprn in ["10023995207"]:  # E164EB -> E138NE : 301 Newham Way, London
            rec["accept_suggestion"] = False

        return rec
