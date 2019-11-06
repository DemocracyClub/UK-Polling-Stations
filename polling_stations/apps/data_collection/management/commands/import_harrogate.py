from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000165"
    addresses_name = "parl.2019-12-12/Version 1/Democracy_Club__12December2019harro.tsv"
    stations_name = "parl.2019-12-12/Version 1/Democracy_Club__12December2019harro.tsv"
    elections = ["parl.2019-12-12"]
    csv_delimiter = "\t"
    allow_station_point_from_postcode = False

    def station_record_to_dict(self, record):

        # Samwaies Hall
        if record.polling_place_id == "13135":
            record = record._replace(polling_place_postcode="")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")
        rec = super().address_record_to_dict(record)

        if uprn == "100052009106":
            rec["postcode"] = "HG3 5AT"

        if record.addressline6.strip() == "YO7 4ED":
            return None

        return rec
