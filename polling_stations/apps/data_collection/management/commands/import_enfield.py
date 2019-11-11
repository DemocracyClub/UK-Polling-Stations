from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E09000010"
    addresses_name = "parl.2019-12-12/Version 1/Democracy_Club__12December2019en.CSV"
    stations_name = "parl.2019-12-12/Version 1/Democracy_Club__12December2019en.CSV"
    elections = ["parl.2019-12-12"]
    allow_station_point_from_postcode = False

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if uprn == "207021414":  # 5 College Close, London, N182X
            rec["postcode"] = "N182XU"

        # 1-4 Avis house, N97BQZ
        if uprn in ["207021452", "207021453", "207021454", "207021455"]:
            rec["postcode"] = "N97BQ"

        if uprn in ["207016774"]:  # FLAT 2 928 HERTFORD ROAD, ENFIELD
            return None

        return rec

    def station_record_to_dict(self, record):

        if record.polling_place_id == "6566":  # Enfield Highway Community Centre
            record = record._replace(polling_place_easting="535189")
            record = record._replace(polling_place_northing="197091")

        if record.polling_place_id == "6648":  # Christ Church Southgate
            record = record._replace(polling_place_address_1="The Green")

        return super().station_record_to_dict(record)
