from data_collection.ems_importers import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E09000004"
    addresses_name = (
        "parl.2019-12-12/Version 1/L B Bexley - Democracy_Club__12December2019.tsv"
    )
    stations_name = (
        "parl.2019-12-12/Version 1/L B Bexley - Democracy_Club__12December2019.tsv"
    )
    elections = ["parl.2019-12-12"]
    csv_delimiter = "\t"
    allow_station_point_from_postcode = False

    def station_record_to_dict(self, record):
        # Point supplied for Footscray Baptist Church is miles off
        if record.polling_place_id == "1804":
            record = record._replace(
                polling_place_easting="547145", polling_place_northing="171147"
            )
        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.lstrip("0")

        if record.addressline6.strip() in ("DA14 6NG", "DA14 6NE"):
            # The only 6NG property should be 6NE, which is itself split across stations in a surprising way
            return None

        if uprn in [
            "10090793686",  # DA74AQ -> DA74QW : 2A Pickford Road, Bexleyheath, Kent
            "100020221033",  # DA14RN -> DA14RS : 23A Iron Mill Lane, Crayford, Kent
            "100020221034",  # DA14RN -> DA14RS : 23 Iron Mill Lane, Crayford, Kent
        ]:
            rec["accept_suggestion"] = True

        if uprn in [
            "100023522937",  # DA68DP -> DA68HZ : 9 Standard Road, Bexleyheath, Kent
        ]:
            rec["accept_suggestion"] = False

        return rec
