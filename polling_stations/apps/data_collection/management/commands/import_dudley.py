from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E08000027"
    addresses_name = "parl.2019-12-12/Version 1/merged.tsv"
    stations_name = "parl.2019-12-12/Version 1/merged.tsv"
    elections = ["parl.2019-12-12"]
    csv_delimiter = "\t"
    csv_encoding = "windows-1252"
    allow_station_point_from_postcode = False

    def station_record_to_dict(self, record):

        # St Andrews District Church
        if record.polling_place_id == "22550":
            record = record._replace(polling_place_postcode="DY3 3AB")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "90146449",  # DY69LJ -> DY69NW : Swan Hotel, Stream Road, Kingswinford, West Midlands
            "90163017",  # DY13EP -> DY11EP : 2 The Old Court House, 3 Priory Street, Dudley, West Midlands
        ]:
            rec["accept_suggestion"] = True

        if uprn in [
            "90153005",  # WV149AR -> WV149LE : Foxgloves, Elmdale Road, Coseley, West Midlands
            "90213042",  # DY81DX -> DY83DF : Flat Above, 78 High Street, Stourbridge, West Midlands
            "90214339",  # B629EN -> B634BN : 23 Hay Barn Close, Halesowen, West Midlands
            "90214017",  # B629EN -> DY84GF : 12 Hay Barn Close, Halesowen, West Midlands
            "90156425",  # B629EJ -> B629LB : 161 Long Lane, Halesowen, West Midlands
        ]:
            rec["accept_suggestion"] = False

        if uprn == "90161895":
            return None

        return rec
