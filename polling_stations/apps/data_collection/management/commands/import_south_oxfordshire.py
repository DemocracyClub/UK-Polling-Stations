from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000179"
    # single file merged for South Oxfordshire and Value of White Horse
    # we'll split out the bits we need
    addresses_name = (
        "parl.2019-12-12/Version 1/Democracy_Club__12December2019vale and ox.CSV"
    )
    stations_name = (
        "parl.2019-12-12/Version 1/Democracy_Club__12December2019vale and ox.CSV"
    )
    elections = ["parl.2019-12-12"]
    csv_delimiter = ","
    allow_station_point_from_postcode = False

    def station_record_to_dict(self, record):
        # discard records in Vale of White Horse
        if record.polling_place_district_reference.startswith(
            "S"
        ) or record.polling_place_district_reference.startswith("X"):
            return None

        if record.polling_place_id == "8737":
            record = record._replace(polling_place_uprn="")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        # discard records in Vale of White Horse
        if record.polling_place_district_reference.startswith(
            "S"
        ) or record.polling_place_district_reference.startswith("X"):
            return None

        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if record.post_code == "OX49 5BZ" or uprn == "100120897264":
            return None

        if uprn == "100120888662":
            rec["postcode"] = "OX14 3DX"

        if uprn == "100120860708":
            rec["postcode"] = "OX11 9UX"

        return rec
