from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E06000051"
    addresses_name = "parl.2019-12-12/Version 1/Democracy_Club__12December2019shrop.tsv"
    stations_name = "parl.2019-12-12/Version 1/Democracy_Club__12December2019shrop.tsv"
    elections = ["parl.2019-12-12"]
    csv_delimiter = "\t"
    allow_station_point_from_postcode = False

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if uprn == "10013137107":
            rec["postcode"] = "SY13 4DL"
            rec["accept_suggestion"] = False

        if uprn == "200003847744":
            rec["postcode"] = "TF10 9AP"
            rec["accept_suggestion"] = False

        if uprn == "100071210835":
            rec["postcode"] = "WV15 6NL"
            rec["accept_suggestion"] = False

        if record.addressline6 in [
            "SY4 3QR",
        ]:
            return None

        return rec

    def station_record_to_dict(self, record):
        if record.polling_place_id == "25637":
            # Stanton Lacy Village Hall, Stanton Lacy, Ludlow
            record = record._replace(polling_place_easting="352573")
            record = record._replace(polling_place_northing="280557")

        if record.polling_place_id == "25543":
            # Farlow & Oreton Village Hall, Fox Hill, Oreton, Kidderminster, Worcs
            record = record._replace(polling_place_easting="364411")
            record = record._replace(polling_place_northing="280033")

        if record.polling_place_id == "26206":
            # Nesscliffe Village Hall
            record = record._replace(
                polling_place_postcode="SY4 1AX", polling_place_uprn="10011838276"
            )

        return super().station_record_to_dict(record)
