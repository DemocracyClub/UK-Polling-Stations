from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000146"
    stations_name = "parl.2019-12-12/Version 1/west-norfolk.gov.uk-1572885849000-.tsv"
    addresses_name = "parl.2019-12-12/Version 1/west-norfolk.gov.uk-1572885849000-.tsv"
    elections = ["parl.2019-12-12"]
    csv_delimiter = "\t"
    allow_station_point_from_postcode = False

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if uprn == "10024107639":
            rec["postcode"] = ""
            rec["accept_suggestion"] = False

        if record.addressline1 == "8 Lions Close":
            rec["postcode"] = "PE38 0AT"

        return rec

    def station_record_to_dict(self, record):

        if record.polling_place_id == "18049":
            record = record._replace(polling_place_postcode="PE14 9QH")
            record = record._replace(polling_place_easting="0")
            record = record._replace(polling_place_northing="0")

        return super().station_record_to_dict(record)
