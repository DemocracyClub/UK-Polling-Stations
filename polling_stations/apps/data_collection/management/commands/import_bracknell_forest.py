from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E06000036"
    addresses_name = (
        "local.2019-05-02/Version 1/Democracy_Club__02May2019 (Bracknell Forest).tsv"
    )
    stations_name = (
        "local.2019-05-02/Version 1/Democracy_Club__02May2019 (Bracknell Forest).tsv"
    )
    elections = ["local.2019-05-02"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):
        if record.polling_place_id == "3901":
            record = record._replace(polling_place_postcode="RG42 4DS")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in []:
            rec["accept_suggestion"] = True

        if uprn in [
            "10022826533"  # RG403DN -> RG403YZ : The Bungalow, Easthampstead Park Crematorium, South Road, WOKINGHAM
        ]:
            rec["accept_suggestion"] = False

        return rec
