from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000149"
    addresses_name = "local.2019-05-02/Version 1/SouthNorfolk2019PollingStation Report for Democracy Club Website.csv"
    stations_name = "local.2019-05-02/Version 1/SouthNorfolk2019PollingStation Report for Democracy Club Website.csv"
    elections = ["europarl.2019-05-23"]
    csv_delimiter = ","

    def station_record_to_dict(self, record):

        # Station change for EU election
        if record.polling_place_id == "9402":
            record = record._replace(polling_place_name="Costessey")
            record = record._replace(polling_place_address_1="Breckland Hall")
            record = record._replace(polling_place_address_2="Breckland Road")
            record = record._replace(polling_place_address_3="New Costessey")
            record = record._replace(polling_place_address_4="")
            record = record._replace(polling_place_postcode="NR5 0RW")
            record = record._replace(polling_place_easting="0")
            record = record._replace(polling_place_northing="0")
            record = record._replace(polling_place_uprn="")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "2630159192",
            "2630101566",
            "2630106361",
            "2630164300",
            "2630122694",
        ]:
            rec = super().address_record_to_dict(record)
            rec["accept_suggestion"] = True
            return rec

        if uprn == "2630153843":
            rec["postcode"] = "NR14 6RJ"
            rec["accept_suggestion"] = False
            return rec

        return rec
