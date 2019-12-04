from data_collection.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "E07000063"
    addresses_name = "parl.2019-12-12/Version 1/polling_station_export-2019-11-22.csv"
    stations_name = "parl.2019-12-12/Version 1/polling_station_export-2019-11-22.csv"
    elections = ["parl.2019-12-12"]
    allow_station_point_from_postcode = False

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "10033267408",  # BN71EL -> BN108PN : 9 A SOUTHDOWN AVENUE, LEWES
            "10033267407",  # BN71EL -> BN108PN : 9 SOUTHDOWN AVENUE, LEWES
        ]:
            rec["accept_suggestion"] = False

        if record.housepostcode in ["RH17 7QH", "BN8 4AA"]:
            return None

        return rec

    def station_record_to_dict(self, record):
        rec = super().station_record_to_dict(record)
        if rec["internal_council_id"] in [
            "38-alciston-and-selmeston-village-hall",
            "45-alfriston-war-memorial-hall",
            "39-berwick-village-hall",
            "40-hayton-baker-hall",
            "41-deanland-wood-social-centre",
            "46-east-dean-village-hall",
            "47-wilmington-village-hall",
            "48-litlington-village-hall",
            "42-polegate-community-centre",
            "43-polegate-community-centre",
            "44-st-georges-church-hall",
        ]:
            # all these have 0 properties assigned
            # and are in Wealden
            # assume these are used for covering
            # the Lewes parliamentary constituency
            # but not local elections
            return None
        return rec
