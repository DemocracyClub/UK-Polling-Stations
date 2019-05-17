from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E06000052"
    addresses_name = "europarl.2019-05-23/Version 2/Democracy_Club__23May2019 -Cornwall- new file.CSV"
    stations_name = "europarl.2019-05-23/Version 2/Democracy_Club__23May2019 -Cornwall- new file.CSV"
    elections = ["europarl.2019-05-23"]
    csv_delimiter = ","

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if uprn == "10003303540":
            rec["postcode"] = "PL15 9PB"

        return rec

    def station_record_to_dict(self, record):

        if record.polling_place_id == "3453":
            record = record._replace(polling_place_uprn="10003300470")

        if record.polling_place_id == "2992":
            record = record._replace(polling_place_uprn="10003065058")
            record = record._replace(polling_place_postcode="PL11 2PQ")

        if record.polling_place_id == "2669":
            record = record._replace(polling_place_uprn="10002694687")
            record = record._replace(polling_place_postcode="PL26 7FH")

        if record.polling_place_id == "3112":
            record = record._replace(polling_place_uprn="10023432417")
            record = record._replace(polling_place_postcode="PL10 1AX")

        if record.polling_place_id == "3578":
            record = record._replace(polling_place_postcode="EX22 6XL")

        return super().station_record_to_dict(record)
