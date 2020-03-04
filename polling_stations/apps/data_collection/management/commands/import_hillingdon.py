from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E09000017"
    addresses_name = "2020-02-19T10:04:28.162348/Democracy_Club__07May2020...TSV"
    stations_name = "2020-02-19T10:04:28.162348/Democracy_Club__07May2020...TSV"
    elections = ["2020-05-07"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):

        if record.polling_place_id == "9241":
            record = record._replace(polling_place_easting="506536")
            record = record._replace(polling_place_northing="181610")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")
        rec = super().address_record_to_dict(record)

        if uprn in [
            "100022832219"  # 1 Elm View House, Shepiston Lane, Hayes, Middlesex
        ]:
            return None

        if uprn == "100023413509":
            rec["postcode"] = "UB10 8AQ"

        if uprn in [
            "10092980468",  # UB33PF -> UB83PF : 9A  10A Carlton Court Bosanquet Close
            "10022805692",  # UB100QB -> UB100BQ : Flat 3  134 Jefferson Court Vine Lane
        ]:
            rec["accept_suggestion"] = True

        return rec
