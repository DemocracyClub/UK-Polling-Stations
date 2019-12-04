from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E06000039"
    addresses_name = (
        "parl.2019-12-12/Version 1/Democracy_Club__12December2019slough.CSV"
    )
    stations_name = "parl.2019-12-12/Version 1/Democracy_Club__12December2019slough.CSV"
    elections = ["parl.2019-12-12"]
    allow_station_point_from_postcode = False

    def station_record_to_dict(self, record):
        if record.polling_place_id == "1000":  # Claycots School [Town Hall]
            record = record._replace(polling_place_easting="0")
            record = record._replace(polling_place_northing="0")
        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "100081042223",
            "10022917421",
        ]:
            rec["accept_suggestion"] = False

        if uprn == "100080321307":
            rec["postcode"] = "SL6 0LG"

        return rec
