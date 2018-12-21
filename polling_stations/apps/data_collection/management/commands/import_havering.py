from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E09000016"
    addresses_name = "local.2018-05-03/Version 1/Democracy_Club__03May2018 Havering.tsv"
    stations_name = "local.2018-05-03/Version 1/Democracy_Club__03May2018 Havering.tsv"
    elections = ["local.2018-05-03"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):

        """
        File supplied contained obviously inaccurate point
        Replace with correction from council
        """
        if record.polling_place_id == "7305":
            record = record._replace(polling_place_easting="550712.13")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn == "100021363119":
            rec = super().address_record_to_dict(record)
            rec["postcode"] = "RM2 5NS"
            return rec

        if uprn == "100021380241":
            rec = super().address_record_to_dict(record)
            rec["postcode"] = "RM7 8NT"
            return rec

        return super().address_record_to_dict(record)
