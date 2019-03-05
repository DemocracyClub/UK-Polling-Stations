from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000086"
    addresses_name = "local.2019-05-02/Version 1/Democracy_Club__02May2019Eastleigh.tsv"
    stations_name = "local.2019-05-02/Version 1/Democracy_Club__02May2019Eastleigh.tsv"
    elections = ["local.2019-05-02"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")
        rec = super().address_record_to_dict(record)

        if uprn == "100060324905":
            return None

        if uprn in [
            "100060294726",  # SO533DA -> SO533HB : 242 Bournemouth Road, Chandler`s Ford, Eastleigh
            "10009593644",  # SO533DA -> SO533AD : Dovecote, Howard Close, Chandler`s Ford, Eastleigh
        ]:
            rec["accept_suggestion"] = True

        return rec

    def station_record_to_dict(self, record):
        if record.polling_place_uprn == "100062644887":
            record = record._replace(polling_place_postcode="SO53 2FT")

        # use UPRN for this one - E/N is in the sea
        if record.polling_place_id == "4095":
            record = record._replace(polling_place_easting="0")
            record = record._replace(polling_place_northing="0")

        return super().station_record_to_dict(record)
