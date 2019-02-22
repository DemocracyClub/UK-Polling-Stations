from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000238"
    addresses_name = (
        "local.2019-05-02/Version 1/Democracy_Club__02May2019 Wychavon-fixed.tsv"
    )
    stations_name = (
        "local.2019-05-02/Version 1/Democracy_Club__02May2019 Wychavon-fixed.tsv"
    )
    elections = ["local.2019-05-02"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn == "10013945401":
            rec = super().address_record_to_dict(record)
            rec["postcode"] = "GL20 7HB"
            return rec

        if uprn == "100120716819":
            rec = super().address_record_to_dict(record)
            rec["postcode"] = "WR7 4PP"
            return rec

        if uprn == "100120698775":
            rec = super().address_record_to_dict(record)
            rec["postcode"] = "WR11 7PT"
            return rec

        if uprn == "100120709729":
            rec = super().address_record_to_dict(record)
            rec["postcode"] = "WR11 7YH"
            return rec

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):

        """
        File supplied contained obviously inaccurate point
        remove it and fall back to geocoding
        """
        if record.polling_place_id == "5075":
            record = record._replace(polling_place_easting="0")
            record = record._replace(polling_place_northing="0")

        if record.polling_place_id == "4927":
            record = record._replace(polling_place_easting="0")
            record = record._replace(polling_place_northing="0")

        return super().station_record_to_dict(record)
