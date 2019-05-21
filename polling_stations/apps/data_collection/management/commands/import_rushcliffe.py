from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000176"
    addresses_name = "europarl.2019-05-23/Version 1/Democracy_Club__23May2019rush.CSV"
    stations_name = "europarl.2019-05-23/Version 1/Democracy_Club__23May2019rush.CSV"
    elections = ["europarl.2019-05-23"]

    def station_record_to_dict(self, record):

        # these co-ordinates were a missing a digit - fixes carried over from local.2019-05-02
        if record.polling_place_id == "4346":  # Bingham Methodist Centre
            record = record._replace(polling_place_easting="470360")
        if record.polling_place_id == "4390":  # Edwalton Church Hall
            record = record._replace(polling_place_easting="459770")
        if record.polling_place_id == "4525":  # West Bridgford Baptist Church
            record = record._replace(polling_place_easting="458380")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if uprn == "3040065651":
            rec["postcode"] = "NG12 4DF"

        if uprn == "3040069418":
            rec["postcode"] = "NG23 5RW"

        return rec
