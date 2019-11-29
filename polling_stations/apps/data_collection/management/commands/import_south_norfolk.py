from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000149"
    addresses_name = "parl.2019-12-12/Version 2/Democracy_Club__12December2019.tsv"
    stations_name = "parl.2019-12-12/Version 2/Democracy_Club__12December2019.tsv"
    elections = ["parl.2019-12-12"]
    csv_delimiter = "\t"
    allow_station_point_from_postcode = False

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if record.addressline6 == "NR18 9FB":
            return None

        if (record.addressline1, record.addressline6) in [
            ("Acers", "NR9 3LT"),
            ("24 Bank Street", "NR18 0BX"),
        ]:
            return None

        if record.addressline6 in [
            "NR14 6TF",
            "NR14 7UU",
        ]:
            return None

        if uprn in [
            "2630159192",
            "2630101566",
            "2630106361",
            "2630164300",
            "2630122694",
        ]:
            rec["accept_suggestion"] = True

        return rec
