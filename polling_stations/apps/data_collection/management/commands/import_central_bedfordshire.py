from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):

    council_id = "E06000056"
    addresses_name = (
        "parl.2019-12-12/Version 2/Democracy_Club__12December2019 polling stations.csv"
    )
    stations_name = (
        "parl.2019-12-12/Version 2/Democracy_Club__12December2019 polling stations.csv"
    )
    elections = ["parl.2019-12-12"]
    csv_delimiter = ","
    allow_station_point_from_postcode = False

    def station_record_to_dict(self, record):

        # Haynes Village Hall
        if record.polling_place_id == "13358":
            record = record._replace(polling_place_easting="510086")
            record = record._replace(polling_place_northing="242021")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        # most of these UPRNs are junk
        if uprn.endswith("0000000"):
            rec["uprn"] = ""

        if record.addressline1 == "Meadow Lake":
            rec["postcode"] = "SG191NU"
        if record.addressline1 in ["4 Bunch O`nuts", "3 Bunch O`nuts"]:
            rec["postcode"] = "LU5 5DX"

        if uprn in [
            "10093351429",
            "10014618845",
        ]:
            return None

        if uprn in [
            "10000861447",  # MK430LN -> MK430LP : 110B Lower Shelton Road, Marston Moretaine, Beds
            "10000799231",  # MK430LN -> MK430LP : 110 Lower Shelton Road, Marston Moretaine, Beds
            "10002278170",  # LU63RG -> LU63JH : Aveldone House, 70-74 Common Road, Kensworth, Dunstable, Beds.
            "10001023325",  # LU55AD -> LU55ES : 48A Houghton Road, Dunstable, Beds.
        ]:
            rec["accept_suggestion"] = False

        return rec
