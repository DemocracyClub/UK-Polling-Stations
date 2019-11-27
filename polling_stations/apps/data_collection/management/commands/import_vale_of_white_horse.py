from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000180"
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
        # discard records in South Oxfordshire
        if record.polling_place_district_reference.startswith(
            "L"
        ) or record.polling_place_district_reference.startswith("R"):
            return None

        # Polling place grid ref wrong.
        if record.polling_place_id in ["8409"]:
            record = record._replace(polling_place_easting="0")
            record = record._replace(polling_place_northing="0")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        # discard records in South Oxfordshire
        if record.polling_place_district_reference.startswith(
            "L"
        ) or record.polling_place_district_reference.startswith("R"):
            return None

        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10093195669"  # OX29AH -> OX29PH : 136, Apt 2, Cumnor Hill, Cumnor, Oxford, Oxfordshire
        ]:
            rec["accept_suggestion"] = True

        if uprn == "10014079091":
            rec["postcode"] = "OX12 0ED"

        if uprn == "10014027599":
            rec["postcode"] = "OX12 8AU"

        if record.post_code == "SN7 8FG":
            return None

        if uprn == "10014082062":
            return None

        return rec
