from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000194"
    addresses_name = "parl.2019-12-12/Version 1/merged.tsv"
    stations_name = "parl.2019-12-12/Version 1/merged.tsv"
    elections = ["parl.2019-12-12"]
    csv_delimiter = "\t"
    csv_encoding = "windows-1252"
    allow_station_point_from_postcode = False

    def station_record_to_dict(self, record):
        if record.polling_place_id == "4925":
            # Guildroom, Guildhall, Bore Street, Lichfield
            record = record._replace(polling_place_postcode="WS13 6LU")
        if record.polling_place_id == "4912":
            # Mobile Polling Station, Staffs University West Car Park, Monks Close, Lichfield
            record = record._replace(
                polling_place_easting=411530, polling_place_northing=309223
            )
        # Locations for these because I investigated why they had the same postcode and it turns out they're adjacent
        # properties
        if record.polling_place_id == "4924":
            # Holy Cross, Community Meeting Room, Holy Cross Church
            record = record._replace(
                polling_place_easting=411921, polling_place_northing=308789
            )
        if record.polling_place_id == "4920":
            # Holy Cross Parish Hall
            record = record._replace(
                polling_place_easting=411908, polling_place_northing=308797
            )
        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10013216157"  # WS70HZ -> WS70HT : The Coach House, Edial House Farm, Lichfield Road, Burntwood, Staffs
        ]:
            rec["accept_suggestion"] = True

        if uprn in [
            "10002777436",  # B783TW -> B783SR : Longwood House, Drayton Manor Park, Tamworth, Staffs
            "10024113376",  # B783TW -> B783TJ : Manor Lodge, Drayton Manor Park, Tamworth, Staffs
            "10013216554",  # WS70BJ -> WS70BG : White Swan, 2 Cannock Road, Burntwood, Staffs
            "100032225996",  # WS140ET -> WS140EU : Hilton Studio, Pouk Lane, Hilton, Lichfield, Staffs
            "100031687250",  # WS70HY -> WS70HZ : Edial House, 415 Lichfield Road, Burntwood, Staffs
            "10013848296",  # WS140EN -> WS140ER : Lynn Lane Farm, Lynn Lane, Shenstone, Lichfield, Staffs
        ]:
            rec["accept_suggestion"] = False

        return rec
