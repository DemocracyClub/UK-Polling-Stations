from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E09000002"
    addresses_name = "europarl.2019-05-23/Version 2/Democracy_2Club__23May2019.tsv"
    stations_name = "europarl.2019-05-23/Version 2/Democracy_2Club__23May2019.tsv"
    elections = ["europarl.2019-05-23"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")
        rec = super().address_record_to_dict(record)

        if record.addressline6.strip() == "RM6 5AN":
            return None

        if record.addressline6.strip() in ["RM9 5DX", "RM9 4DX"]:
            return None

        if uprn == "100012133":
            rec["postcode"] = "RM8 1DJ"
            rec["accept_suggestion"] = False

        if uprn in [
            "100041457",  # RM108BX -> RM109BX : 17 Dunchurch House, Ford Road, Dagenham, Essex
            "100033020",  # RM81BJ -> RM66RJ : 464A Whalebone Lane North, Chadwell Heath, Romford, Essex
        ]:
            rec["accept_suggestion"] = True

        return rec
