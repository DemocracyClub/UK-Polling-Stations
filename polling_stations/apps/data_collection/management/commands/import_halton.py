from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E06000006"
    addresses_name = (
        "parl.2019-12-12/Version 1/Democracy_Club__12December2019halton.tsv"
    )
    stations_name = "parl.2019-12-12/Version 1/Democracy_Club__12December2019halton.tsv"
    elections = ["parl.2019-12-12"]
    csv_delimiter = "\t"
    allow_station_point_from_postcode = False

    def station_record_to_dict(self, record):

        if record.polling_place_id == "1564":  # Scout Hut, Hall Avenue, Widnes
            record = record._replace(polling_place_postcode="WA8 4PU")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)

        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10090873193",  # Flat 1 Victoria House, 20 Ann Street West
            "100010231610",  # Flat 2, 1 South Road, Runcorn
        ]:
            rec["accept_suggestion"] = False

        if uprn in ["10010612061", "10010612062", "10010612064"]:
            rec = super().address_record_to_dict(record)
            rec["postcode"] = "WA7 6HG"
            return rec

        return rec
