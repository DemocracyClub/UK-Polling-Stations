from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E06000051"
    addresses_name = "europarl.2019-05-23/Version 1/Democracy_Club__23May2019shrop.tsv"
    stations_name = "europarl.2019-05-23/Version 1/Democracy_Club__23May2019shrop.tsv"
    elections = ["europarl.2019-05-23"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if uprn == "10013137107":
            rec["postcode"] = "SY13 4DL"
            rec["accept_suggestion"] = False

        if uprn == "200003847744":
            rec["postcode"] = "TF10 9AP"
            rec["accept_suggestion"] = False

        return rec

    def station_record_to_dict(self, record):

        if record.polling_place_id == "23953":
            record = record._replace(polling_place_easting="352573")
            record = record._replace(polling_place_northing="280557")

        if record.polling_place_id == "23961":
            record = record._replace(polling_place_easting="364411")
            record = record._replace(polling_place_northing="280033")

        return super().station_record_to_dict(record)
