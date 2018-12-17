from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E09000015"
    addresses_name = "local.2018-05-03/Version 1/Democracy_Club__03May2018 Harrow 1.tsv"
    stations_name = "local.2018-05-03/Version 1/Democracy_Club__03May2018 Harrow 1.tsv"
    elections = ["local.2018-05-03"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):

        if record.polling_place_name[-1] == ",":
            record = record._replace(polling_place_name=record.polling_place_name[:-1])

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn == "100023030633":
            rec = super().address_record_to_dict(record)
            rec["postcode"] = "HA2 9JE"
            return rec

        return super().address_record_to_dict(record)
