from data_collection.management.commands import (
    BaseXpressDCCsvInconsistentPostcodesImporter,
)


class Command(BaseXpressDCCsvInconsistentPostcodesImporter):
    council_id = "E06000056"
    addresses_name = "local.2019-05-02/Version 2/Democracy_Club__02May2019CB.CSV"
    stations_name = "local.2019-05-02/Version 2/Democracy_Club__02May2019CB.CSV"
    elections = ["local.2019-05-02"]
    csv_delimiter = ","

    def station_record_to_dict(self, record):

        if record.polling_place_id == "10177":
            record = record._replace(polling_place_easting="0")
            record = record._replace(polling_place_northing="0")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "100081004693",  # LU55DZ -> LU55DX : 4 Bunch O`nuts, The Green, Houghton Regis, Dunstable, Beds.
            "100081004692",  # LU55DZ -> LU55DX : 3 Bunch O`nuts, The Green, Houghton Regis, Dunstable, Beds.
        ]:
            rec["accept_suggestion"] = True

        if uprn in [
            "10000861447",  # MK430LN -> MK430LP : 110B Lower Shelton Road, Marston Moretaine, Beds
            "10000799231",  # MK430LN -> MK430LP : 110 Lower Shelton Road, Marston Moretaine, Beds
            "100081000463",  # MK453QT -> MK452AZ : Apple Tree Cottage, Maulden Woods, Maulden, Bedford
            "10002278170",  # LU63RG -> LU63JH : Aveldone House, 70-74 Common Road, Kensworth, Dunstable, Beds.
            "10001023325",  # LU55AD -> LU55ES : 48A Houghton Road, Dunstable, Beds.
            "100081006449",  # LU79PU -> LU79PY : Tudor Cottage, 2 Dunstable Road, Tilsworth, Leighton Buzzard, Beds.
        ]:
            rec["accept_suggestion"] = False

        if record.addressline6 == "SG18 OJS":
            rec["postcode"] = "SG180JS"

        return rec
