from data_importers.management.commands import BaseHalarose2026UpdateCsvImporter


class Command(BaseHalarose2026UpdateCsvImporter):
    council_id = "GLG"
    addresses_name = "2026-05-07/2026-03-25T14:15:29.329144/GLG_combined.csv"
    stations_name = "2026-05-07/2026-03-25T14:15:29.329144/GLG_combined.csv"
    elections = ["2026-05-07"]

    def station_record_to_dict(self, record):
        if "LINTHAUGH NURSERY" in record.pollingstationname:
            record = record._replace(
                pollingstationpostcode=record.pollingstationaddress5
            )
            record = record._replace(pollingstationaddress5="")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "906700531273",  # UNIT 508B 47 KYLE STREET, GLASGOW
            "906700531270",  # UNIT 507H 47 KYLE STREET, GLASGOW
            "906700496057",  # FLAT 0/1 18 GREAT GEORGE STREET, GLASGOW
        ]:
            return None

        if record.postcode in [
            # split
            "G14 9HQ",
            "G20 8NH",
            "G21 2LN",
            "G22 6RL",
            "G3 8AY",
            "G33 3SU",
            "G34 0DN",
            "G52 1RZ",
            "G53 6UW",
            "G61 1QE",
            # suspect
            "G51 2WU",
            "G51 2WX",
            "G51 2YJ",
        ]:
            return None
        return super().address_record_to_dict(record)
