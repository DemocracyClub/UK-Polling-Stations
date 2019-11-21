from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000069"
    addresses_name = (
        "parl.2019-12-12/Version 1/Democracy_Club__12December2019castle.tsv"
    )
    stations_name = "parl.2019-12-12/Version 1/Democracy_Club__12December2019castle.tsv"
    elections = ["parl.2019-12-12"]
    csv_delimiter = "\t"
    allow_station_point_from_postcode = False

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")
        rec = super().address_record_to_dict(record)

        if uprn in [
            "10004934986",
            "100090361765",
            "10004940667",
            "10004941055",
        ]:
            return None

        if record.addressline1 == "Caravan 1112A Thorney Bay Park":
            rec["postcode"] = "SS8 0DB"
        if uprn == "10004937052":
            rec["postcode"] = "SS8 7SL"

        return rec
