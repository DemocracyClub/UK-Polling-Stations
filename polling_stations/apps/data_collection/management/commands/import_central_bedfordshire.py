from data_collection.management.commands import (
    BaseXpressDCCsvInconsistentPostcodesImporter,
)


class Command(BaseXpressDCCsvInconsistentPostcodesImporter):
    council_id = "E06000056"
    addresses_name = (
        "europarl.2019-05-23/Version 1/Democracy_Club__23May2019centbed.CSV"
    )
    stations_name = "europarl.2019-05-23/Version 1/Democracy_Club__23May2019centbed.CSV"
    elections = ["europarl.2019-05-23"]
    csv_delimiter = ","

    def station_record_to_dict(self, record):

        # Haynes Village Hall
        if record.polling_place_id == "11179":
            record = record._replace(polling_place_easting="510086")
            record = record._replace(polling_place_northing="242021")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        # most of these UPRNs are junk
        if uprn.endswith("0000000"):
            rec["uprn"] = ""

        if record.addressline1 in ["4 Bunch O`nuts", "3 Bunch O`nuts"]:
            rec["postcode"] = "LU5 5DX"

        if uprn in [
            "10000861447",  # MK430LN -> MK430LP : 110B Lower Shelton Road, Marston Moretaine, Beds
            "10000799231",  # MK430LN -> MK430LP : 110 Lower Shelton Road, Marston Moretaine, Beds
            "10002278170",  # LU63RG -> LU63JH : Aveldone House, 70-74 Common Road, Kensworth, Dunstable, Beds.
            "10001023325",  # LU55AD -> LU55ES : 48A Houghton Road, Dunstable, Beds.
        ]:
            rec["accept_suggestion"] = False

        if record.addressline6 == "SG18 OJS":
            rec["postcode"] = "SG180JS"

        return rec
