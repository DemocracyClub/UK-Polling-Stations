from data_collection.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "E07000063"
    addresses_name = (
        "local.2019-05-02/Version 1/polling_station_export-2019-02-18Lewes.csv"
    )
    stations_name = (
        "local.2019-05-02/Version 1/polling_station_export-2019-02-18Lewes.csv"
    )
    elections = ["local.2019-05-02"]

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "10033267408",  # BN71EL -> BN108PN : 9 A SOUTHDOWN AVENUE, LEWES
            "10033267407",  # BN71EL -> BN108PN : 9 SOUTHDOWN AVENUE, LEWES
        ]:
            rec["accept_suggestion"] = False

        if record.housepostcode == "RH17 7QH":
            return None

        return rec

    def station_record_to_dict(self, record):
        rec = super().station_record_to_dict(record)
        if rec["internal_council_id"] in [
            "62-alciston-and-selmeston-village-hall",
            "69-alfriston-war-memorial-hall",
            "63-berwick-village-hall",
            "64-hayton-baker-hall",
            "65-deanland-wood-social-centre",
            "70-east-dean-village-hall",
            "71-wilmington-village-hall",
            "72-litlington-village-hall",
            "66-polegate-community-centre",
            "67-polegate-community-centre",
            "68-st-georges-church-hall",
        ]:
            # all these have 0 properties assigned
            # and are in Wealden
            # assume these are used for covering
            # the Lewes parliamentary constituency
            # but not local elections
            return None
        return rec
