from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E09000028"
    addresses_name = (
        "parl.2019-12-12/Version 1/Democracy_Club__12December2019_Southwark_V2.TSV"
    )
    stations_name = (
        "parl.2019-12-12/Version 1/Democracy_Club__12December2019_Southwark_V2.TSV"
    )
    elections = ["parl.2019-12-12"]
    csv_delimiter = "\t"
    csv_encoding = "windows-1252"
    allow_station_point_from_postcode = False

    def station_record_to_dict(self, record):

        # Osprey Tenants Hall
        if record.polling_place_id == "11775":
            record = record._replace(polling_place_easting="535832")
            record = record._replace(polling_place_northing="178848")

        # Cossall Tenants Hall
        if record.polling_place_id == "11854":
            record = record._replace(polling_place_easting="534747")
            record = record._replace(polling_place_northing="176505")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)

        uprn = record.property_urn.strip().lstrip("0")

        if record.addressline2 == "179 Forest Hill Road":
            return None

        if record.addressline6 in [
            "SE16 2EZ",
            "SE21 7BG",
            "SE1 0AA",
            "SE1 0NS",
            "SE1 6SB",
            "SE15 4TP",
        ]:
            return None

        if uprn in [
            "10094086807",
            "200003480357",
            "10093341595",
            "10093341594",
            "10093341119",
            "10090283768",
            "10094086939",
            "10090747304",
            "10093340214",
            "10009806727",
            "10094086331",
            "10094743182",
        ]:
            return None

        if uprn in ["200003487670", "200003487907"]:
            rec["postcode"] = "SE1 2BB"

        if uprn == "10090283768":
            rec["postcode"] = "SE1 3UN"

        if uprn == "10093341734":
            rec["postcode"] = "SE1 6PS"

        if uprn == "10091665680":
            rec["uprn"] = ""
            rec["postcode"] = "SE5 0EZ"

        if uprn in ["10093341594", "10093341595"]:
            rec["postcode"] = "SE1 2BX"

        if uprn == "10093340235":
            rec["postcode"] = "SE22 9EE"

        if uprn == "10091664197":
            rec["postcode"] = "SE22 9PP"

        if uprn == "10090750130":
            rec["postcode"] = "SE1 5AD"

        return rec
