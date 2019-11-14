from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000086"
    addresses_name = "parl.2019-12-12/Version 1/Parliamentary Election - Democracy_Club__12December2019east.tsv"
    stations_name = "parl.2019-12-12/Version 1/Parliamentary Election - Democracy_Club__12December2019east.tsv"
    elections = ["parl.2019-12-12"]
    csv_delimiter = "\t"
    allow_station_point_from_postcode = False

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")
        rec = super().address_record_to_dict(record)

        # Implausible looking UPRN geocodes. Throw away rather than investigate.
        if uprn in [
            "10091136033",
            "100060322293",
            "10091136173",
            "10009593531",
            "10012197923",
        ]:
            return None

        if uprn in [
            "100060294726",  # SO533DA -> SO533HB : 242 Bournemouth Road, Chandler`s Ford, Eastleigh
            "10009593644",  # SO533DA -> SO533AD : Dovecote, Howard Close, Chandler`s Ford, Eastleigh
            "100060302836",  # SO532FG -> SO535BZ : 138 Kingsway, Chandler`s Ford, Eastleigh
            "10009589400",  # SO507DE -> SO507DF : The Chalet, Moon River Pines, Fir Tree Lane, Horton Heath, Eastleigh
            "10091136799",  # SO303FA -> SO532HL : 8a Clanfield Close, Chandler`s Ford, Eastleigh
        ]:
            rec["accept_suggestion"] = True

        return rec

    def station_record_to_dict(self, record):
        if record.polling_place_id == "4629":  # Abbey Hall, Victoria Road.
            record = record._replace(polling_place_easting="445232")
            record = record._replace(polling_place_northing="108734")

        if (
            record.polling_place_uprn == "100062644887"
        ):  # Chandler's Ford Community Centre
            record = record._replace(polling_place_postcode="SO53 2FT")

        return super().station_record_to_dict(record)
