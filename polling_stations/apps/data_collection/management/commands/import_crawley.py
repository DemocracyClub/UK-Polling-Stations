from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000226"
    addresses_name = "local.2019-05-02/Version 2/Democracy_Club__02May2019.tsv"
    stations_name = "local.2019-05-02/Version 2/Democracy_Club__02May2019.tsv"
    elections = ["local.2019-05-02"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if record.addressline6 == "RH10 3HW":
            rec["postcode"] = "RH10 3GW"

        if uprn in [
            "10024122201"  # RH110EA -> RH110AE : 50A Ifield Drive, Ifield, Crawley
        ]:
            rec["accept_suggestion"] = True

        return rec

    def station_record_to_dict(self, record):
        if record.polling_place_id == "675":
            record = record._replace(polling_place_easting="526564")
            record = record._replace(polling_place_northing="135576")
        if record.polling_place_id == "692":
            record = record._replace(polling_place_easting="528408")
            record = record._replace(polling_place_northing="135808")
        return super().station_record_to_dict(record)
