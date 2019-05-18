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

        # most of these UPRNs are junk
        if uprn.endswith("00000"):
            rec["uprn"] = ""

        if uprn == "10003303540":
            rec["postcode"] = "PL15 9PB"

        if record.addressline6.strip() in [
            "PL15 9NR",
            "EX23 9PX",
            "TR4 8JA",
            "PL15 7SN",
            "EX23 9PJ",
            "PL15 7SL",
            "TR19 6LJ",
        ]:
            return None

        return rec

    def station_record_to_dict(self, record):

        # Methodist Sunday School Room
        if record.polling_place_id == "3453":
            record = record._replace(polling_place_uprn="10003300470")

        # The Cove Hall, Wilcove
        if record.polling_place_id == "2992":
            record = record._replace(polling_place_uprn="10003065058")
            record = record._replace(polling_place_postcode="PL11 2PQ")

        # St Austell Rugby Club
        if record.polling_place_id == "2669":
            record = record._replace(polling_place_uprn="10002694687")

        # Millbrook Village Hall
        if record.polling_place_id == "3112":
            record = record._replace(polling_place_uprn="10023432417")

        return super().station_record_to_dict(record)
