from data_collection.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "E08000016"
    addresses_name = (
        "local.2018-05-03/Version 1/Democracy Club - Polling Districts Barnsley.CSV"
    )
    stations_name = (
        "local.2018-05-03/Version 1/Democracy Club - Polling Stations Barnsley.CSV"
    )
    elections = ["local.2018-05-03", "mayor.sheffield-city-ca.2018-05-03"]

    def address_record_to_dict(self, record):

        if record.uprn == "100050685041":
            rec = super().address_record_to_dict(record)
            rec["postcode"] = "S35 7AJ"
            return rec

        if record.postcode == "S70 5UD":
            return None

        return super().address_record_to_dict(record)
