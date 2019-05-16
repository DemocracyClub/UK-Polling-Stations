from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E09000015"
    addresses_name = "europarl.2019-05-23/Version 1/Democracy_Club__23May2019.csv"
    stations_name = "europarl.2019-05-23/Version 1/Democracy_Club__23May2019.csv"
    elections = ["europarl.2019-05-23"]
    csv_delimiter = ","

    def station_record_to_dict(self, record):

        if record.polling_place_name[-1] == ",":
            record = record._replace(polling_place_name=record.polling_place_name[:-1])

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")
        rec = super().address_record_to_dict(record)

        if uprn == "10091092216":
            rec["postcode"] = "HA2 0LH"

        if uprn in ["10070264489", "10091094715", "10091094714"]:
            rec["accept_suggestion"] = False

        return rec
