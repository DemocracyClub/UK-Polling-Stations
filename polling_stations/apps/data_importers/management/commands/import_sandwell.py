from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "SAW"
    addresses_name = (
        "2022-05-05/2022-02-21T14:46:13.389652/Democracy_Club__05May2022.tsv"
    )
    stations_name = (
        "2022-05-05/2022-02-21T14:46:13.389652/Democracy_Club__05May2022.tsv"
    )
    elections = ["2022-05-05"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")
        rec = super().address_record_to_dict(record)

        if uprn in [
            "10093004484",  # FLAT THE DOVECOTE HILL TOP, WEST BROMWICH B70 0SD
            "100071578415",  # 622A BEARWOOD ROAD, SMETHWICK B664DP
            "32072080",  # 251 HOLYHEAD ROAD, WEDNESBURY WS107DQ
            "32072081",  # 253 HOLYHEAD ROAD, WEDNESBURY WS107DQ
        ]:
            return None

        if record.addressline6 in [
            "B64 7JA",
            "B65 0BS",
            "B67 7EP",
            "B70 8DB",
            "DY4 9NB",
            "B71 4HS",
            "DY4 7TY",
            "B66 4DP",
        ]:
            return None

        if record.post_code == "B70 OSH":
            rec["postcode"] = "B700SH"
        if record.post_code == "B68 OLH":
            rec["postcode"] = "B680LH"

        return rec
