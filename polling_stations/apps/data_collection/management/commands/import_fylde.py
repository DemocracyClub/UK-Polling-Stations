from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000119"
    addresses_name = "local.2019-05-02/Version 1/Fylde-Democracy_Club__02May2019.csv"
    stations_name = "local.2019-05-02/Version 1/Fylde-Democracy_Club__02May2019.csv"
    elections = ["local.2019-05-02"]
    match_threshold = 98

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in ("200001037742", "200001037759"):
            rec = super().address_record_to_dict(record)
            rec["postcode"] = "PR4 0RL"
            return rec

        if uprn == "100012391142":
            rec = super().address_record_to_dict(record)
            rec["postcode"] = "PR4 0RN"
            return rec

        if uprn == "200001128516":
            rec = super().address_record_to_dict(record)
            rec["postcode"] = "FY6 9BU"
            return rec

        if uprn in [
            "10013591588",
            "100010405565",
            "100012620334",
            "100010399571",
            "100012619511",
            "100012620275",
            "100012618650",
            "100010401469",
        ]:
            rec = super().address_record_to_dict(record)
            rec["accept_suggestion"] = True
            return rec

        return super().address_record_to_dict(record)
