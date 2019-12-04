from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E06000052"
    addresses_name = "parl.2019-12-12/Version 1/Democracy_Club__12December2019corn.tsv"
    stations_name = "parl.2019-12-12/Version 1/Democracy_Club__12December2019corn.tsv"
    elections = ["parl.2019-12-12"]
    csv_delimiter = "\t"
    allow_station_point_from_postcode = False

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if "Roundhouse Way" in record.addressline1:
            rec["postcode"] = "TR13 8WL"

        if uprn == "10003303540":
            rec["postcode"] = "PL15 9PB"

        if record.addressline6.strip() in [
            "EX23 9PJ",
            "TR20 9JG",
        ]:
            return None

        if uprn in ["10014484586"]:
            return None

        return rec

    def station_record_to_dict(self, record):

        # Methodist Sunday School Room
        if record.polling_place_id == "4637":
            record = record._replace(polling_place_uprn="10003300470")
        # The Cove Hall, Wilcove
        if record.polling_place_id == "4768":
            record = record._replace(polling_place_uprn="10003065058")
            record = record._replace(polling_place_postcode="PL11 2PQ")

        # St Austell Rugby Club
        if record.polling_place_id == "5003":
            record = record._replace(
                polling_place_uprn="10002694687", polling_place_postcode="PL26 7FH"
            )

        # Millbrook Village Hall
        if record.polling_place_id == "4891":
            record = record._replace(
                polling_place_uprn="10023432417", polling_place_postcode="PL10 1AX"
            )

        return super().station_record_to_dict(record)
